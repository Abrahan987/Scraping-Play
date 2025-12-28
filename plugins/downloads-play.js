import fetch from "node-fetch"
import yts from 'yt-search'
import ytdl from 'ytdl-core'

const handler = async (m, { conn, text, usedPrefix, command }) => {
try {
if (!text.trim()) return conn.reply(m.chat, `❀ Por favor, ingresa el nombre de la música a descargar.`, m)
await m.react('🕒')

const videoMatch = text.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/|live\/|v\/))([a-zA-Z0-9_-]{11})/)
const query = videoMatch ? 'https://youtu.be/' + videoMatch[1] : text
const search = await yts(query)
const result = videoMatch ? search.videos.find(v => v.videoId === videoMatch[1]) || search.all[0] : search.all[0]
if (!result) throw 'ꕥ No se encontraron resultados.'

const { title, thumbnail, timestamp, views, ago, url, author, seconds } = result
if (seconds > 1800) throw '⚠ El contenido supera el límite de duración (10 minutos).'

const vistas = formatViews(views)
const info = `「✦」Descargando *<${title}>*\n\n> ❑ Canal » *${author.name}*\n> ♡ Vistas » *${vistas}*\n> ✧︎ Duración » *${timestamp}*\n> ☁︎ Publicado » *${ago}*\n> ➪ Link » ${url}`

// Send info and thumbnail first for instant feedback
const thumb = (await conn.getFile(thumbnail)).data
await conn.sendMessage(m.chat, { image: thumb, caption: info }, { quoted: m })

// Now, fetch the media and send it
const isAudio = ['play', 'yta', 'ytmp3', 'playaudio'].includes(command)
const isVideo = ['play2', 'ytv', 'ytmp4', 'mp4'].includes(command)

const media = await (isAudio ? getAud(url) : getVid(url))

if (!media?.url) {
  await m.react('✖️')
  return m.reply(`⚠ No se pudo obtener el enlace de descarga para ${isAudio ? 'audio' : 'video'}.`)
}

m.reply(`> ❀ *${isAudio ? 'Audio' : 'Vídeo'} procesado. Servidor:* \`${media.api}\``)

if (isAudio) {
  await conn.sendMessage(m.chat, { audio: { url: media.url }, fileName: `${title}.mp3`, mimetype: 'audio/mpeg' }, { quoted: m })
} else if (isVideo) {
  await conn.sendFile(m.chat, media.url, `${title}.mp4`, `> ❀ ${title}`, m)
}

await m.react('✔️')
} catch (e) {
  await m.react('✖️')
  return conn.reply(m.chat, typeof e === 'string' ? e : '⚠︎ Se ha producido un problema.\n> Usa *' + usedPrefix + 'report* para informarlo.\n\n' + e.message, m)
}}

handler.command = handler.help = ['play', 'yta', 'ytmp3', 'play2', 'ytv', 'ytmp4', 'playaudio', 'mp4']
handler.tags = ['descargas']
handler.group = true

export default handler

async function getAud(url) {
  try {
    const info = await ytdl.getInfo(url);
    const format = ytdl.chooseFormat(info.formats, { quality: 'highestaudio' });
    return { url: format.url, api: 'ytdl-core' };
  } catch (e) {
    console.error(`Failed to get audio URL: ${e.message}`);
    return null;
  }
}

async function getVid(url) {
  try {
    const info = await ytdl.getInfo(url);
    const format = ytdl.chooseFormat(info.formats, { quality: 'highestvideo' });
    return { url: format.url, api: 'ytdl-core' };
  } catch (e) {
    console.error(`Failed to get video URL: ${e.message}`);
    return null;
  }
}
function formatViews(views) {
if (views === undefined) return "No disponible"
if (views >= 1_000_000_000) return `${(views / 1_000_000_000).toFixed(1)}B (${views.toLocaleString()})`
if (views >= 1_000_000) return `${(views / 1_000_000).toFixed(1)}M (${views.toLocaleString()})`
if (views >= 1_000) return `${(views / 1_000).toFixed(1)}k (${views.toLocaleString()})`
return views.toString()
}
