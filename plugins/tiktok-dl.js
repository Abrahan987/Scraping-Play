import { tiktok } from '../lib/tiktok.js';

const handler = async (m, { conn, text, usedPrefix, command }) => {
  if (!text) {
    return conn.reply(m.chat, `Por favor, ingresa un enlace de TikTok. Ejemplo: ${usedPrefix + command} https://vm.tiktok.com/XYZ/`, m);
  }

  const urlRegex = /https?:\/\/(www\.)?tiktok\.com\/[^\s]+/g;
  if (!urlRegex.test(text)) {
    return conn.reply(m.chat, 'Por favor, ingresa un enlace de TikTok válido.', m);
  }

  try {
    await m.react('🕒');
    const result = await tiktok(text);

    if (!result || !result.videoUrl) {
      await m.react('✖️');
      return conn.reply(m.chat, 'No se pudo obtener el video de TikTok.', m);
    }

    await conn.sendFile(m.chat, result.videoUrl, 'tiktok.mp4', result.text, m);
    await m.react('✔️');
  } catch (error) {
    await m.react('✖️');
    console.error('Error in TikTok plugin:', error);
    conn.reply(m.chat, 'Ocurrió un error al procesar la solicitud.', m);
  }
};

handler.command = handler.help = ['tiktok', 'ttdl'];
handler.tags = ['descargas'];
handler.group = true;

export default handler;
