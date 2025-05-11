package com.vocabo.app

class LlamaInterface {
    external fun initLlama(modelPath: String): String

    companion object {
        init {
            System.loadLibrary("llama-lib")
        }
    }
}
