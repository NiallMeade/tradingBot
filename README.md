# tradingBot
Automated python stock trading bot.

The trading strategy copys the trades of "insiders" in various different companies in USA markets, http://openinsider.com/.

Test.py in openInsiderTest takes in a history of insider trades from a csv file and iterates through each one. It retrieves the closest available price of the relevant stock from yahoo finance at the time the trade was made public. The stock price a day later is also retrieved. All these start and finish prices are exported to a csv file to get an aveage growth or loss. This test claims an average return of about 2% growth per trade with a hold time of a day.

SeleniumTest and TradeFinder attempt to execute this strategy using the Trading212 broker platform. Selenium must be used to manipulate the browser as there is no Trading212 api at the moment. SeleniumTest has scripts that were designed to test buy, sell, and BuyAmount functions. TradeFinder.py takes these funtions and executes them with the latests trades from http://openinsider.com/ as their arguemnts. Unfortunatley, I only found out after developing these scripts that Trading212 generally only trades "blue chip stocks" (the more popular ones). The majority of the stocks I was trying the buy were penny stocks so they could not be bought on Trading212.

I pivoted to the Degiro platform, adapting my selenium funtions for their website, again they don't have an api. The script was succesfull, i ran it for a week splitting my portfolio over 3 different stocks at a time.

I found in practice this strategy wasn't succesfull, at least not on Degiro with the funds I had. I had a loss of 2 euro after 15+ trades with 300 euro of available funds. Degiro charges over a euro per trade for commission, so without these fees the strategy is profitable, it also becomes more profitable with more funds.
