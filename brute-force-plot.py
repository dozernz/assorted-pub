#!/usr/bin/env python3
# Plots chance of sucessful brute force over multiple "attempts"
# For example, guessing a TOTP code, password reset token, or similar where the correct value is fixed, but time to guess is limited
# Assumes chance between attempts is independent

# Example: 100 req/s , 30 minutes window to guess code, code is 6 char hex
# Probability of getting it in one attempt (over full time window) is:
#   100 req/s * 30*60 seconds = 180000
#   search space is 16^6 (a-f0-9) to the power of number of characters = 16777216
#   probability = 180000 / 16777216 = 0.0107.. or 1.07%
#
# This is the probability of sucess in a single atetmpts. If we make 20 attempts (30 mins each):
#   this gives us ~ 19.41% chance of correct guess with 10 hours of bruteforcing
#   however with 48 attempts (24 hours), this chance increases to 40%
#   If longer is possible, guessing over 3 days (144 attempts) gives a 78.8% chance of a successful guess!
#
# This can be a signifcant risk if the account is high privileged, and the brute forcing is unnoticed

from scipy.stats import binom
import matplotlib.pyplot as plt

rps = 100
seconds = 30*60
charset_size = 16
num_chars = 6

probability = ( rps * seconds ) / (charset_size**num_chars)
attempts = 144 #3 days
attempt_range = list(range(attempts))


y_arr = []
for i in range(1,attempts+1):
    output = binom.pmf(0, i, probability)
    y_arr.append(output)

print(f"Chance of sucess after {attempts} attempts is: {(1-output)*100:.2f}%")
print(f"This can be attempted in {attempts*seconds} seconds or {attempts*seconds/3600} hours")

#want to calculate the chance of sucess not failure
#so subtract from 1 and multiply by 100 for percent
y = list(map(lambda x: (1 - x)*100, y_arr))
x = list(range(1,attempts+1))

plt.xlabel("Number of attempts")
plt.ylabel("Chance of success")
plt.title(f"Chance of success over multiple attempts ({attempts*seconds/3600} hours)")

#Format units on axis
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))

#50% chance axis
plt.axhline(50,color="red",linestyle="--")

#plot and show
plt.plot(x,y)
plt.show()
#plt.savefig('/tmp/output.png')
