package com.example

import com.example.plugins.configureRouting
import com.example.plugins.configureSerialization
import io.ktor.http.*
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.plugins.logging.*
import io.ktor.client.request.*
import io.ktor.serialization.gson.*
import io.ktor.server.application.*
import kotlinx.coroutines.*
import net.dv8tion.jda.api.JDABuilder
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.hooks.ListenerAdapter
import net.dv8tion.jda.api.requests.GatewayIntent


val client = HttpClient(CIO) {
    install(ContentNegotiation) {
        gson()
    }
    install(Logging) {
        logger = Logger.DEFAULT
        level = LogLevel.INFO
    }
}

suspend fun sendMessage(webhookUrl: String, message: String) {
    client.post(webhookUrl) {
        contentType(ContentType.Application.Json)
        setBody(mapOf("content" to message))
    }
    println("Message sent")
}

val applicationScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

class BotListener(private val webhookUrl: String) : ListenerAdapter() {
    private val botPrefix = "@zadanie-3"

    override fun onMessageReceived(event: MessageReceivedEvent) {
        if (event.author.isBot) return
        val messageContent = event.message.contentDisplay
        if (!messageContent.contains(botPrefix)) return
        val author = event.author.name

        val response = """
            |--------------------------------
            |Received Message Directed to Bot:
            |Author: $author
            |Content: $messageContent
            |--------------------------------
        """.trimMargin()

        println(response)

    }
}

fun startBot(token: String, webhookUrl: String) {
    val jda = JDABuilder.createDefault(token)
        .enableIntents(GatewayIntent.MESSAGE_CONTENT)
        .addEventListeners(BotListener(webhookUrl))
        .build()
    jda.awaitReady()
    println("Bot is ready!")
}

fun main() = runBlocking {

    val botToken = "MTIyNDM5MzcyNzczNzU5ODE1NQ.Glb8Th.ZJ0S6YFd-gfm7oyDLNO8foldDjabJ-Ep-q_TT0"
    val webhookUrl = "https://discord.com/api/webhooks/1224413982023094382/5G7MHtQSk_ot_txXkpl0B6DF4wTrgAHSSSFBVV0C9vlxOWYDenWX0IlZWbXTPCA3L97_"
    startBot(botToken, webhookUrl)

    val message = "Hello from exercise 3!"
    sendMessage(webhookUrl, message)
    client.close()
}



fun Application.module() {
    configureSerialization()
    configureRouting()
}









