package com.vocabo.app

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.vocabo.app.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private val llamaInterface = LlamaInterface()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.testButton.setOnClickListener {
            val result = llamaInterface.initLlama("/path/to/model.bin")
            binding.resultText.text = result
        }
    }
}
