# -*- coding:utf-8 -*-

from __future__ import print_function
import frida
import sys
import tempfile

def yuv420p_to_mp4(yuvbuffer,width,height,stride,padding):
  pass

session = frida.attach("Player v2 Helper")    // Electron application process
script = session.create_script("""


///////////////////////////////////////////////////////////////////

var baseAddr = Module.findBaseAddress("Electron Framework");      

print("Electron Framework baseAddress is at :"+baseAddr);

//!!!!!!!!!!!!!!!!!!!! You need modify CdmWrapperImpl hardcode address before hook   !!!!!!!!!!!!!!!!////////


 var CdmWrapperImpl_Decrypt=baseAddr.add(0x6feb60);                   //CdmWrapperImpl::Decrypt hardcode Address

 var CdmWrapperImpl_DecryptAndDecodeFrame=baseAddr.add(0x6febe0);     //CdmWrapperImpl::DecryptAndDecodeFrame hardcode Address


////////////////////////////////////////////////////////////////////////////////////////////////////////
 var CdmDecryptFunc = new NativeFunction(ptr(CdmWrapperImpl_Decrypt),       //CDM->Decrypt
    
    'int', [ 'pointer','pointer','pointer' ]);

 var CdmDecryptAndDecodeFunc = new NativeFunction(ptr(CdmWrapperImpl_DecryptAndDecodeFrame),       //CDM->DecryptAndDecode
    
    'int', [ 'pointer','pointer','pointer' ]);

 //////////////////////////////////////Print Module info//////////////////////////////////////////////////
 print("CdmWrapperImpl::DecryptAndDecodeFrame Address is at :0x"+CdmWrapperImpl_DecryptAndDecodeFrame.toString(16));

 print("CdmWrapperImpl::Decrypt Address is at :0x"+CdmWrapperImpl_Decrypt.toString(16));

 ////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////Costumn Function list///////////////////////////////////////

    function PrintBuffer(addr,size,info)
{
/*
    var arryData=Memory.readByteArray(ptr(addr),size);

    var array = new Uint8Array(arryData);

    //var TempData=info+' ->'+addr +' :['

    var TempData=info+' :'+"\033[35m"+'['
    
    for(var i = 0; i < array.length; ++i){
          TempData+=(array[i].toString(16));
          TempData+=",";
        }
     var dumpData=TempData.substr(0,TempData.length-1)+']';

        print("   " +dumpData);
*/

}

    function print(info)
{
    console.log("\033[33m"+info);
}

    function tracelog(info)
{
    console.log("\033[32m"+info);
}


Interceptor.attach(ptr(CdmWrapperImpl_Decrypt), {
        onEnter: function(args) {


        tracelog("Cdm::Decrypt  is called ! " );

      this.decrypted_block= args[2] ;


    },
    onLeave:function(retval){
    
//**********************************************Get DecryptedBlock->Buffer Data *********************************************

   
    var ptrDecryptedBlockBuffer=Memory.readPointer(this.decrypted_block.add(0x8));  //get  DecryptedBlockImpl->buffer_  
       
    var GetDecryptDataAddr=Memory.readPointer(ptr(Memory.readPointer(ptrDecryptedBlockBuffer)).add(0x10));  // DecryptedBuffer()->Data() 

    var GetDecryptDataSizeAddr=Memory.readPointer(ptr(Memory.readPointer(ptrDecryptedBlockBuffer)).add(0x20));  // DecryptedBuffer()->Size() 


    var GetDecryptDataFunc = new NativeFunction(ptr(GetDecryptDataAddr),
        'int64', ['pointer']);

    var GetDecryptDataSizeFunc = new NativeFunction(ptr(GetDecryptDataSizeAddr),
        'int64', ['pointer']);

    ////********************************************** Call Buffer->Data() and Size() **************************************************
        
    var DecryptData= GetDecryptDataFunc( ptr(ptrDecryptedBlockBuffer));                //call Buffer->Data() 


    var DecryptDataSize= GetDecryptDataSizeFunc( ptr(ptrDecryptedBlockBuffer));        // call Buffer()->Size()
 

    var arryData=Memory.readByteArray(ptr(DecryptData),Number(DecryptDataSize));


    send("Audio", arryData);

    //PrintBuffer("0x"+DecryptData.toString(16),32,'AudioData['+DecryptDataSize+']');

     }
});

//****************************************** Hook Cdm::DecryptAndDecodeVideo *************************************************************

    //tracelog('Cdm::DecryptAndDecodeVideo address ->'+CdmDecryptAndDecodeVideoFunc+ '  is hooked !' );

Interceptor.attach(ptr(CdmWrapperImpl_DecryptAndDecodeFrame), {

    onEnter: function(args) {

        tracelog("Cdm::DecryptAndDecodeVideo  is called ! " );    

/*
        //PrintBuffer(data,size,'   Encrypt Video data: ');

        var EncryptionScheme= Memory.readU32(ptr(args[1]).add(12));

          console.log("   EncryptionScheme : "+EncryptionScheme);

        var key_id= Memory.readPointer(ptr(args[1]).add(16));
          console.log("   key_id : "+Memory.readPointer(key_id));

        var key_id_size= Memory.readU32(ptr(args[1]).add(24));
          console.log("   key_id_size : "+key_id_size);

        var padding= Memory.readU32(ptr(args[1]).add(28));

        var iv= Memory.readPointer(ptr(args[1]).add(32));
          console.log("   iv : "+Memory.readPointer(iv));

        var iv_size= Memory.readU32(ptr(args[1]).add(40));
          console.log("   iv_size : "+iv_size);

        //PrintBuffer(inputData,64,'input_buffer ');

*/
        this.video_frame= args[2] ;


 
    },

//********************************************** Get VideoFrame Buffer Data *********************************************

    onLeave:function(retval){

        var ptrVideoFrameBuffer=Memory.readPointer(this.video_frame.add(0x20));  //get  VideoFrameImpl->frame_buffer_  
       

        //PrintBuffer(this.video_frame,64,"Video FrameBuffer  info is :")

       
/*
        print("     Format  : "+Memory.readU32(this.video_frame.add(16)));

        //PrintBuffer(this.video_frame.add(20),4,"  ColorSpace  : ");

        print("     Size  : "+Memory.readU32(this.video_frame.add(24))+' x '+Memory.readU32(this.video_frame.add(28)));

        //print("     Buffer Address  : "+Memory.readPointer(this.video_frame.add(32)));

        print("     PlaneOffSet Y  : "+Memory.readU32(this.video_frame.add(40)));

        print("     PlaneOffSet U  : "+Memory.readU32(this.video_frame.add(44)));

        //Memory.writeU32(this.video_frame.add(48),0);

        print("     PlaneOffSet V  : "+Memory.readU32(this.video_frame.add(48)));

        print("     Stride Y  : "+Memory.readU32(this.video_frame.add(52)));

        print("     Stride U  : "+Memory.readU32(this.video_frame.add(56)));

        print("     Stride V  : "+Memory.readU32(this.video_frame.add(60)));

        print("     Timestamp : "+(Math.floor(Memory.readS64(this.video_frame.add(64)))/1000000)+' s');


*/
        print("     Timestamp : "+(Math.floor(Memory.readS64(this.video_frame.add(64)))/1000000)+' s');


        var GetDecryptDataAddr=Memory.readPointer(ptr(Memory.readPointer(ptrVideoFrameBuffer)).add(0x10));  //get VideoFrameImpl->frame_buffer_->Data()  address

        var GetDecryptDataSizeAddr=Memory.readPointer(ptr(Memory.readPointer(ptrVideoFrameBuffer)).add(0x20));  //get VideoFrameImpl->frame_buffer_->Size()  address

        var GetDecryptDataFunc = new NativeFunction(ptr(GetDecryptDataAddr),
        'int64', ['pointer']);

        var GetDecryptDataSizeFunc = new NativeFunction(ptr(GetDecryptDataSizeAddr),
        'int64', ['pointer']);

//********************************************** Call Buffer->Data() and Size() **********************************************

        
        var DecryptData= GetDecryptDataFunc( ptr(ptrVideoFrameBuffer));             //call VideoFrameImpl->frame_buffer_->Data() 


        var DecryptDataSize= GetDecryptDataSizeFunc( ptr(ptrVideoFrameBuffer));     //call VideoFrameImpl->frame_buffer_->Size() 

      
        var arryData=Memory.readByteArray(ptr(DecryptData),Number(DecryptDataSize));


        PrintBuffer("0x"+DecryptData.toString(16),32,'VidoeData['+DecryptDataSize+']');

        send("Video", arryData);


       // ptr(DecryptData).writeByteArray(logo);
            



     }

});

});



""" )# % int(sys.argv[1], 16))

def on_message(message, data):
   
    if data != None:
        #print(message)
        #print(hex(len(data)))%
        if(message['payload']=='Audio'):
            f=open('a.aac','ab')   #save the acc stream to file.
            f.write(data)
            f.close()
        elif (message['payload']=='Video'):
            #yuv420p_to_mp4(data,720,404,832,8) #compress the yuv420p stream with x264.
            f=open('v.yuv','ab')   #save the decoded yuv stream to file.
            f.write(data);
            f.close()




script.on('message', on_message)
#script.on('write', on_write)

script.load()

try:
  sys.stdin.read()
except KeyboardInterrupt:
  archive.close()
