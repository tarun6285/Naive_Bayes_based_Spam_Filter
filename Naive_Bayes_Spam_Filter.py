import argparse
import math

ham_words = 0.0
spam_words = 0.0
ham_prob = 0.0
spam_prob = 0.0
spamdict = {}
ham_dict = {}


def train_classifier(train_file):
    global ham_words, spam_words, spamdict, \
        ham_dict, ham_prob, spam_prob

    total_mails = 0.0
    ham_mails = 0.0
    spam_mails = 0.0

    with open(train_file, 'r') as training:
        mails = training.readlines()
        for mail in mails:
            words = mail.split(' ')
            total_mails += 1
            if words[1] == 'ham':
                ham_mails += 1  # Count the number of ham mails in the train data
                i = 2
                while i < len(words):
                    ham_words += 1  # count the total number of words in ham mails
                    key = words[i]
                    val = words[i + 1]
                    if key not in ham_dict:  # check whether words exists in ham dictionary
                        ham_dict[key] = float(val)  # add the new word in ham dict along with count
                    else:
                        ham_dict[key] += float(val)  # else increase the value of the existing word
                    i += 2
            if words[1] == 'spam':
                spam_mails += 1  # count the number of spam mails in the train data
                i = 2
                while i < len(words):
                    spam_words += 1  # count the total number of words in spam mail
                    key = words[i]
                    val = words[i + 1]
                    if key not in spamdict:  # check whether words exists in spam dictionary
                        spamdict[key] = float(val)  # add the new word in spam dict along with count
                    else:
                        spamdict[key] += float(val)  # else increase the value of the existing word
                    i += 2
    # Now we calculate the prior probability of ham and spam words in train data
    spam_prob = spam_words / (spam_words + ham_words)
    ham_prob = 1 - spam_prob

    print "\nTraining Set Statistics: "
    print "Total Mails:", total_mails
    print "No. of Ham Mails:", ham_mails
    print "No. of Spam Mails:", spam_mails
    print "Total Words in Ham Mails:", ham_words
    print "Unique Words in Ham Mails:", len(ham_dict)
    print "Total Words in Spam Mails:", spam_words
    print "Unique Words in Spam Mails:", len(spamdict)
    print "Spam Probability:", spam_prob
    print "Ham Probability", ham_prob


# Probabilities are calculated using logs to prevent underflow problem of multiple small multiplications
def naive_bayes(words_list):
    spam = float(1.0)
    ham = float(1.0)
    alpha = 1.0  # Use this value for smoothing
    j = 2
    spam += math.log10(spam_prob)  # Get prior probability of spam from test data
    ham += math.log10(ham_prob)

    while j < len(words_list):
        key1 = words_list[j]

        if key1 in spamdict:  # check each word if it exists in our spam dictionary
            value = spamdict[key1]  # Get the value of the word from our dictionary
            spam += math.log10(value / spam_words) * float(words_list[j+1])  # calculate the new probability
        else:
            # if word not found in spam dictionary we apply smoothing
            spam += math.log10(alpha / spam_words + len(spamdict))

        if key1 in ham_dict:  # check each word if it exists in our ham dictionary
            value = ham_dict[key1]  # Get the value of the word from our dictionary
            ham += math.log10(value / ham_words) * float(words_list[j+1])  # calculate the new probability
        else:
            # if word not found in spam dictionary we apply smoothing
            ham += math.log10(alpha / ham_words + len(ham_dict))
        j += 2
    return spam, ham


def test_classifier(test_file):
    given_spam = 0.0
    given_ham = 0.0
    predham = 0.0
    predspam = 0.0
    match = 0.0
    ham_match = 0.0
    spam_match = 0.0
    test_mails = 0.0
    out = open(output, "w")

    with open(test_file, 'r') as testing:
        mails = testing.readlines()
        for mail in mails:
            words = mail.split(' ')
            test_mails += 1  # count the number of mails for testing
            given_class = words[1]  # Actual class of test mail
            if given_class == 'spam':
                given_spam += 1  # Count number of spam mails in the test file
            if given_class == 'ham':
                given_ham += 1  # Count the number of ham mails in test file
            spam_pp, ham_pp = naive_bayes(words)  # Calculate spam and ham probability for each mail

            if ham_pp > spam_pp:  # If ham probability is greater than spam
                pred_class = 'ham'  # Predict the mail as ham
                var1 = ",ham" + "\n"
                out.write(words[0] + var1)  # Write output to out file
                predham += 1  # Count number of predicted ham mails
            else:
                pred_class = 'spam'  # Predict mail as spam
                var2 = ",spam" + "\n"
                out.write(words[0] + var2)
                predspam += 1  # Count the number of predicted spam mails

            if pred_class == given_class and given_class == 'ham':
                match += 1  # Count total number of correctly predicted mails
                ham_match += 1  # Count number of correctly predicted ham mails
            if pred_class == given_class and given_class == 'spam':
                match += 1
                spam_match += 1  # Count number of correctly predicted spam mails
    out.close()

    print "\n\nTest Set Results:"
    print "Total emails classified :", test_mails
    print "Number of emails correctly classified :", match
    print "Accuracy of classifier :", match / test_mails * 100.0, "%"
    print "Precision :", spam_match / predspam * 100, "%"
    print "Recall is :", spam_match / given_spam * 100, "%"


if __name__ == "__main__":
    read = argparse.ArgumentParser()
    read.add_argument('-f1')
    read.add_argument('-f2')
    read.add_argument('-o')

    args = read.parse_args()
    args = vars(args)
    train = args['f1']
    test = args['f2']
    output = args['o']

    train_classifier(train)
    test_classifier(test)
