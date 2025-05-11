#include <jni.h>
#include <string>
#include <android/log.h>

#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, "LlamaInterface", __VA_ARGS__)

extern "C" JNIEXPORT jstring JNICALL
Java_com_vocabo_app_LlamaInterface_initLlama(
        JNIEnv* env,
        jobject /* this */,
        jstring modelPath) {
    
    const char* path = env->GetStringUTFChars(modelPath, 0);
    LOGD("Initializing Llama with model: %s", path);
    
    // TODO: Add actual llama.cpp initialization here
    
    env->ReleaseStringUTFChars(modelPath, path);
    return env->NewStringUTF("Llama initialized successfully");
}
