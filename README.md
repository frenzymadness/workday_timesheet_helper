# WorkDay timesheet helper

I am releasing the first version of the time sheet helper for WorkDay!

Disclaimer: It's very naive, pre-alpha version, requires some manual work and nobody should use it. But it works for me :)

License: WTFPLv2 https://en.wikipedia.org/wiki/WTFPL#Version_2

It works on weekly basis so either you specify which week you want to fill or it does it for the current week.
So, to fill the time sheet for the third week in July, run `python3 workday.py -w 29`.

It's not able to detect any kind of PTO (public holidays, sick days, annual leave, …) and WorkDay freely lets you
to save duplicated entries. In cases when you need to skip some days in a week, pass them as a comma separated list
(of numbers like 0 for Monday or short names like mon) to the script. For example, the second week in July had public
holiday on Monday and I had a sick day on Wednesday so to skip those two days and fill the rest
I used `python workday.py -w 28 -s 0,2`. This should not apply to situations when a month starts or ends in the middle
of a week because previous and next months should be locked already.

It randomizes the times as the previous version for Orange did but does it once for a whole week.
Feel free to update the scripts to your needs.

Requirements:

1. selenium working with Firefox (geckodriver)
1. working Kerberos in the browser with a valid ticket

Patches and testers are welcome.