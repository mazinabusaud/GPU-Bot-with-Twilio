import time
from datetime import datetime #datetime/time is used to prevent spam messages
from datetime import timedelta
from requests_html import HTMLSession #used to check stock
import os
from twilio.rest import Client #used for sending texts


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'xxx'
auth_token = 'xxx'
client = Client(account_sid, auth_token)


#3070 links
evgaXC3_3070_link = "https://www.bestbuy.com/site/evga-geforce-rtx-3070-xc3-ultra-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6439299.p?skuId=6439299"
msi_TrioX_3070_link = "https://www.bestbuy.com/site/msi-nvidia-geforce-rtx-3070-gaming-x-trio-8gb-gddr6-pci-express-4-0-graphics-card/6438279.p?skuId=6438279"
msi_trioZ_3070_link = "https://www.bestbuy.com/site/msi-nvidia-geforce-rtx-3070-gaming-z-trio-lhr-8gb-gddr6-pci-express-4-0-graphics-card-black/6471285.p?skuId=6471285"
nvidia_3070_link = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442"
gigaEagle_3070_link = "https://www.bestbuy.com/site/gigabyte-nvidia-geforce-rtx-3070-eagle-8gb-gddr6-pci-express-4-0-graphics-card/6437912.p?skuId=6437912"

#3060 links
evgaXC_3060_link = "https://www.bestbuy.com/site/evga-nvidia-geforce-rtx-3060-xc-gaming-12gb-gddr6-pci-express-4-0-graphics-card/6454329.p?skuId=6454329"
msiVentus_3060_link = "https://www.bestbuy.com/site/msi-nvidia-geforce-rtx-3060-ventus-2x-12g-oc-12gb-gddr6-pci-express-4-0-graphics-card-black/6462173.p?skuId=6462173"
nvidia_3060_link = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402"

testerLink = "https://www.bestbuy.com/site/apple-airpods-pro-white/5706659.p?skuId=5706659" #for testing purposes on in stock items
gpuLinks = [evgaXC3_3070_link, msi_TrioX_3070_link, msi_trioZ_3070_link, nvidia_3070_link, gigaEagle_3070_link, evgaXC_3060_link, msiVentus_3060_link, nvidia_3060_link]
lastHourDateTime = datetime.now() - timedelta(hours = 3) 
timers = [lastHourDateTime] * 8 #used to keep track of last time notification was sent for each GPU

numberArray = ['xxx','xxx'] #input your phone numbers in here

newSession = HTMLSession()

#function to text whenever a GPU comes into stock
def textNotify(about,link):
    for number in numberArray:
        message = client.messages \
        .create(
            from_='+xxx',
            to=number,
            body=f'{about.text} is in stock! {link}'
        )

#main function; scans through each GPU link and checks if it is in stock
def main():
    while True:
        now = datetime.now()
        overBreak = False
        # print(now)
        for i,link in enumerate(gpuLinks):
            pager = newSession.get(link)
            if pager.html.find('.btn-primary.btn-lg',first = True) == None:
                itemName = pager.html.find('.sku-title',first = True).text
                print(f"{itemName} is Sold Out!")
            else:
                time_elapsed = datetime.now() - timers[i]
                if time_elapsed.seconds >= 300:
                    timers[i] = datetime.now()
                    about = pager.html.find('.sku-title',first = True)
                    textNotify(about,link)
                    print(f"{about.text} is in stock!")

if __name__ == "__main__":
    main()