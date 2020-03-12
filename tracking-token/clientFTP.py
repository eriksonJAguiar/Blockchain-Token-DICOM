from ftplib import FTP
import os
import time

files = ['0c1aae2e8ace423c377b717fd02d42e6c2d42f94c08432f6dfa69cf92321929a.zip', '0db6d1b6548dfaab4b75819ab1d1a5a33158bb6d98f6ee383be29288e912f7e8.zip', '10f35ee6f16df0d1313ca54f8c5f4bd31613e3c06d910dd62e0cccbf5158a02f.zip', '1a52128b6f987389e4de9089c5b888239f69a072ed9c15b6bf3b13ec1c7b9332.zip', '1a989fbe87aa3d414af2a2ae04f6df9d4094a8dba0a57ade65f1639fdea29e47.zip', '1e20ae162580d96c31e574b0c4b0804f2dd0c2d9030bf93f60592ca5ce572002.zip', '29e8482a41ea29eaaf6ab4d7f4b623131407c147fa9913f6bf12db451bbd03c0.zip', '384199b29edd0ea70493f38d0d85d3d849458f5b89300a12b35610e7203cd5c8.zip', '47fdddb82d118754cae0a458eedd1fe368bacfe2802f988ec0e0b245482171c9.zip', '49189893ac5708e0d1430c5337959c7613c75d2848268cf6bd1abe77a80362d4.zip', '540bb4e38de9c4846407a47e21269213aab4a09f2c4b52e9bbd8e47c6844fd74.zip', '5b427d1fd8c2ae3b27b638af49e9f7f35ba418dda642f5a4da2b2d84b0e65efb.zip', '698303ebb2b3aa7ad703dccbc609557767af82939422f9afc21a95cd0f0d67f9.zip', '786535ce22f880679628020e5e57188b63d5144f983088cbd76cbe765a02e1c8.zip', '8c90d4a2975e69e415871a72e6a60db744801f532397379698a112fe4c872121.zip', '96392b03d8db69a0020a0bc464ee387cff97fba34aa6647f176e0b978ebc01a9.zip', 'b4faf9b3762f4c1504c743ab57352adf550b8f23d6a0d07b2e2a1fc434300357.zip', 'bd51383b4a1b7e15033c2468c6e0333423efd0defad37c47595a45c93bbe8cb8.zip', 'c155bcd31a3e347012372a409f9d27ee800cb9e51e72e134d17a641547e63f5b.zip', 'f7dd45a3781ce3c68fd9b0ac34ee4817476e2afea1f15fa458e7497a14ee1ec5.zip']

def ftpget():
    os.makedirs('./SharedDicom', exist_ok=True)
    ftp = FTP()
    ftp.connect('10.62.9.185', 1026)
    ftp.login('user','12345')
    start_time_file = time.time()
    for filename in files:
            fname = filename.split('/')
            fname = fname[len(fname)-1]
            fpath = os.path.join('./SharedDicom', fname)
            with open(fpath, 'wb') as f:
                    ftp.retrbinary('RETR %s' % fname, f.write)
                    print('Done ..')
            time.sleep(10)
            ftp.quit()
            tf = time.time()-start_time_file
            print(tf)

if __name__ == '__main__':
   ftpget()
