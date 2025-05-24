const { makeWASocket, useMultiFileAuthState, DisconnectReason } = require("@whiskeysockets/baileys");
const qrcode = require("qrcode-terminal");
const axios = require("axios");

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
      const response = await axios.post("http://localhost:8002/message", {
        message: texto,
      });

      const reply = response.data.response || "🤖 Não entendi.";

      await sock.sendMessage(from, { text: reply });
    } catch (err) {
      console.error("Erro:", err.message);
      await sock.sendMessage(from, { text: "⚠️ Erro ao chamar a API." });
    }
  });
}

startBot();
