# Creator: QI NIU
# This file is to scrape the apartment information from Zillow.com in order to help people find a place to live.

import requests
import parsel
import csv
import time

# Create csv file to save data
f = open('Zillow.csv', mode='w', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    'Title',
    'Address',
    'Price',
    'Type',
])
csv_writer.writeheader()

# Get user input for address
address_input = input(
    'Please input the address you want to live(for example: san diego ca): ')
formatted_address = address_input.replace(' ', '-').lower()


# Send request to get data
headers = {
    'Cookie': 'x-amz-continuous-deployment-state=AYABeAML2j83E6qQk7cZYogV2wIAPgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3MjU1NjcyMVRZRFY4RDcyVlpWAAEAAkNEABpDb29raWUAAACAAAAADN+HuYv%2FZszkJWl1OAAwMkIsSoqL6YxGxtT4GNb35zueQNw21mHYxJ7cRdxnMPAvMyl%2FvEd6yKkVaSW1g0%2FhAgAAAAAMAAQAAAAAAAAAAAAAAAAAAIdwachfXPyacReV69mFbQ7%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAAAy1XVCGtCo+Bss3T13EhYTqH7RW1QLIEqHFPARp; zguid=24|%2407b3dada-24d7-4e50-9e62-d14d0f2988b1; zgsession=1|c8f8c9f3-312c-49c3-ae12-cf1f11cde7e6; pxcts=fe810098-afe5-11ee-8e77-3dedbcced7fc; _pxvid=fe80f503-afe5-11ee-8e77-21f1e0254463; zjs_anonymous_id=%2207b3dada-24d7-4e50-9e62-d14d0f2988b1%22; zjs_user_id=null; zg_anonymous_id=%22cef6b19c-8ebd-494a-830d-8ae637c689a2%22; JSESSIONID=736076FF08DE70CAD9DB27957070B90D; _ga=GA1.2.1354610927.1706686141; _gid=GA1.2.1009908547.1706686141; _gcl_au=1.1.1937924426.1706686143; DoubleClickSession=true; _uetsid=68bf36e0c00a11eea23617d05699df20; _uetvid=e3fe06a0512511eea4b8c5b369e88f8e; __pdst=f048b72125464faaba34a1fe39a95e6d; _fbp=fb.1.1706686143559.691776584; _pin_unauth=dWlkPVlqVXpaalk1WVRBdE9EQTVOaTAwWmpnMkxXRTNZV0l0TVdSa016ZzRNVEl5Wm1aaw; tfpsi=4c2761c5-4d7b-450e-9adc-6e3c91ba2030; _clck=vukyxk%7C2%7Cfiv%7C0%7C1491; __gads=ID=d8c9363f21addc5b:T=1706686142:RT=1706686668:S=ALNI_MbpyI_uaIoeQLaUbVKbu79OttPHUw; __gpi=UID=00000a0a3769bbd1:T=1706686142:RT=1706686668:S=ALNI_MaWJPDWAciU_8IoXbnqhyf0vOC63A; x-amz-continuous-deployment-state=AYABeFNadbfzhZpgU0uoyWiQ+7EAPgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3MjU1NjcyMVRZRFY4RDcyVlpWAAEAAkNEABpDb29raWUAAACAAAAADGkp2gQyL++69CaRVwAwHNHq6i4YERp3026D8BV+Li6%2FMIVC4BwgALFQUMZlbSsuAQRv24kHBFrU7v1DFg6uAgAAAAAMAAQAAAAAAAAAAAAAAAAAAFgkaz7qDDe2vJztzWRZilb%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAAAzU8Ow34ux50M3xxwdhmbngHIERGGxWvjQyvoWtGGxWvjQyvoWtGGxWvjQyvoWtGGxWvjQyvoWt; _clsk=z48nb4%7C1706686736247%7C7%7C0%7Cw.clarity.ms%2Fcollect; _gat=1; AWSALB=WSchK8hVrlu7N/Dxd86JhSjA7U6N5VzeKkFh3nPPx0QZDJThUhuNBTrLRDiPlPKD857YnzASRImgNn0/Lnl7OCSqyrUqTUWYgFxIEpn4asi6Dwlr6C5GGSXehp8+; AWSALBCORS=WSchK8hVrlu7N/Dxd86JhSjA7U6N5VzeKkFh3nPPx0QZDJThUhuNBTrLRDiPlPKD857YnzASRImgNn0/Lnl7OCSqyrUqTUWYgFxIEpn4asi6Dwlr6C5GGSXehp8+; search=6|1709278962384%7C%09%0940415%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

for page in range(1, 10):
    print(f'============Searching for Page: {page}============')
    if page == 1:
        url = f'https://www.zillow.com/{formatted_address}/rentals/'
    else:
        url = f'https://www.zillow.com/{formatted_address}/rentals/{page}_p/'
    response = requests.get(url=url, headers=headers)
    # print(response.status_code)  test if the request is successful
    html_data = response.text
    selector = parsel.Selector(html_data)

    # Extract all li in the required class
    lis = selector.css(
        'li.ListItem-c11n-8-84-3__sc-10e22w8-0.StyledListCardWrapper-srp__sc-wtsrtn-0.iCyebE.gTOWtl')
    
    # Extract the information from each li
    for li in lis:
        if li.css('.jnnxAW address::text').get() is None:
            continue
        houseInfo = li.css('.jnnxAW address::text').get().split(' | ')
        title = houseInfo[0]
        if len(houseInfo) > 1:
            address = houseInfo[1]
        else:
            title = houseInfo[0].split(', ')[0]
            address = houseInfo[0].split(', ')[1:]
            address = ', '.join(address)
        price = li.css('.iMKTKr::text').get().split('+ ')[0]
        price_num = price.replace('$', '').replace(',', '')
        if "/mo" or "+" in price_num:
            price_num = price_num.replace('/mo', '').replace('+', '')
        type = li.css('.iMKTKr::text').get().split('+ ')[-1]
        if type == price:
            type = 'Not indicated'

        # Write the information into the csv file as dictionary
        dit = {
            'Title': title,
            'Address': address,
            'Price': price_num,
            'Type': type,
        }
        csv_writer.writerow(dit)
        print(dit)
    time.sleep(10)