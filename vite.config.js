import { defineConfig } from 'vite';
import { copyFileSync } from 'fs';
import { resolve } from 'path';

export default defineConfig({
  server: {
    host: '0.0.0.0',
    port: 5173
  },
  build: {
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split('.');
          const ext = info[info.length - 1];
          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(ext)) {
            return `assets/images/[name]-[hash][extname]`;
          } else if (/css/i.test(ext)) {
            return `assets/css/[name]-[hash][extname]`;
          }
          return `assets/[name]-[hash][extname]`;
        }
      }
    }
  },
  plugins: [
    {
      name: 'copy-static-files',
      closeBundle() {
        try {
          copyFileSync(resolve(__dirname, 'sitemap.xml'), resolve(__dirname, 'dist/sitemap.xml'));
          copyFileSync(resolve(__dirname, 'robots.txt'), resolve(__dirname, 'dist/robots.txt'));
          console.log('Copied sitemap.xml and robots.txt to dist/');
        } catch (err) {
          console.warn('Could not copy static files:', err.message);
        }
      }
    }
  ]
});
