import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Ukrainian Kodi",
  description: "Awesome ukrainian addons for Kodi",
  base: '/repository.ukrainian',
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Головна', link: '/' },
      { text: 'Аддони', link: '/addons/plugin.video.eneyida' }
    ],

    sidebar: [
      {
        text: 'Аддони',
        items: [
          { text: 'plugin.video.eneyida', link: '/addons/plugin.video.eneyida' },
          { text: 'plugin.video.unimay', link: '/addons/plugin.video.unimay' },
        ]
      },
      {
        text: 'Налаштування',
        items: [
          { text: 'Встановлення через репозиторий', link: '/install/repo' },
          { text: 'Встановлення напряму', link: '/install/addon' },
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/CakesTwix/repository.ukrainian' }
    ]
  }
})
