# WideVineDump
Dump audio and video streams from  Widevine Level 3 with a frida script .

# Notice:

You need to find and replace the [CdmWrapper::Decrypt](https://cs.chromium.org/chromium/src/media/cdm/cdm_wrapper.h?l=120&gs=kythe%253A%252F%252Fchromium.googlesource.com%252Fchromium%252Fsrc%253Flang%253Dc%25252B%25252B%253Fpath%253Dsrc%252Fmedia%252Fcdm%252Fcdm_wrapper.h%2523oRrt7BkNzFrd-h6XXuy_hYlcOIQRIFSef4ZubD3MV9I&gsn=Decrypt&ct=xref_usages) and [CdmWrapper::DecryptAndDecodeFrame](https://cs.chromium.org/chromium/src/media/cdm/cdm_wrapper.h?l=128&gs=kythe%253A%252F%252Fchromium.googlesource.com%252Fchromium%252Fsrc%253Flang%253Dc%25252B%25252B%253Fpath%253Dsrc%252Fmedia%252Fcdm%252Fcdm_wrapper.h%2523OyH1-jImaoPuQvlpYCt7AUAWU5ib2BQ-bBUzbuRVrRw&gsn=DecryptAndDecodeFrame&ct=xref_usages) function hardcode address in the script before dump.

![image](https://img-blog.csdnimg.cn/20191228181026132.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3RlcnJ5MTIwMQ==,size_16,color_FFFFFF,t_70)
