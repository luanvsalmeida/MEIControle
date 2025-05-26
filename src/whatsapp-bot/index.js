const { makeWASocket, useMultiFileAuthState, DisconnectReason } = require("@whiskeysockets/baileys");
const qrcode = require("qrcode-terminal");
const axios = require("axios");
const fs = require("fs");
const path = require("path");

async function startBot() {
  const { state, saveCreds } = await useMultiFileAuthState("./auth_info");

  const sock = makeWASocket({
    auth: state
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", ({ connection, qr }) => {
    if (qr) {
      console.log("📱 Escaneie o QR code abaixo com o WhatsApp:");
      qrcode.generate(qr, { small: true });
    }

    if (connection === "open") {
      console.log("✅ Bot conectado ao WhatsApp!");
    }

    if (connection === "close") {
      console.log("❌ Conexão fechada, reconectando...");
      startBot();
    }
  });

  sock.ev.on("messages.upsert", async ({ messages }) => {
    const msg = messages[0];
    if (!msg.message || msg.key.fromMe) return;

    const texto = msg.message.conversation || "";
    const from = msg.key.remoteJid;

    console.log("📩 Mensagem recebida:", texto);

    try {
      const response = await axios.post("http://localhost:8002/api/message", {
        chatId: 1, 
        userId: 1,
        role: "user",
        content: texto,
      });

      console.log("📤 Resposta da API:", response.data);

      const apiResponse = response.data;
      const reply = apiResponse.content || apiResponse.message || "🤖 Não entendi.";

      // Send text message first
      await sock.sendMessage(from, { text: reply });

      // Check if there's a chart to send (image)
      if (apiResponse.chart) {
        try {
          const chartPath = apiResponse.chart;
          // Convert absolute API path to HTTP URL
          // Remove /code/api from path and use /static endpoint
          const relativePath = chartPath.replace('/code/api/static', '/static');
          const chartUrl = `http://localhost:8002${relativePath}`;
          
          console.log("📊 Baixando gráfico:", chartUrl);
          
          // Download the image from API
          const chartResponse = await axios.get(chartUrl, {
            responseType: 'arraybuffer'
          });
          
          await sock.sendMessage(from, {
            image: Buffer.from(chartResponse.data),
            caption: "📊 Gráfico do relatório financeiro"
          });
          
          console.log("✅ Gráfico enviado com sucesso!");
          
        } catch (chartError) {
          console.error("❌ Erro ao enviar gráfico:", chartError.message);
          await sock.sendMessage(from, { 
            text: "⚠️ Erro ao enviar o gráfico." 
          });
        }
      }

      // Check if there's a report to send (CSV file)
      if (apiResponse.report) {
        try {
          const reportPath = apiResponse.report;
          // Convert absolute API path to HTTP URL
          // Remove /code/api from path and use /static endpoint
          const relativePath = reportPath.replace('/code/api/static', '/static');
          const reportUrl = `http://localhost:8002${relativePath}`;
          
          console.log("📄 Baixando relatório CSV:", reportUrl);
          
          // Download the CSV from API
          const reportResponse = await axios.get(reportUrl, {
            responseType: 'arraybuffer'
          });
          
          const fileName = path.basename(reportPath);
          
          await sock.sendMessage(from, {
            document: Buffer.from(reportResponse.data),
            fileName: fileName,
            mimetype: "text/csv",
            caption: "📄 Relatório financeiro em CSV"
          });
          
          console.log("✅ Relatório CSV enviado com sucesso!");
          
        } catch (reportError) {
          console.error("❌ Erro ao enviar relatório:", reportError.message);
          await sock.sendMessage(from, { 
            text: "⚠️ Erro ao enviar o relatório CSV." 
          });
        }
      }

    } catch (err) {
      console.error("❌ Erro na API:", err.message);
      await sock.sendMessage(from, { text: "⚠️ Erro ao chamar a API." });
    }
  });
}

startBot();