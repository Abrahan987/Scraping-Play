import { tiktokdl } from '@bochilteam/scraper';

const tiktok = async (url) => {
  try {
    const { video } = await tiktokdl(url);
    const result = {
      videoUrl: video.no_watermark,
      text: 'Tiktok scraper By ABRAHAN-M\nSea.qhññ'
    };
    return result;
  } catch (error) {
    console.error('Error in TikTok scraper:', error);
    return null;
  }
};

export { tiktok };
