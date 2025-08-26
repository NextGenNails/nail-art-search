import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
        <style dangerouslySetInnerHTML={{
          __html: `
            @font-face {
              font-family: 'PP Eiko';
              src: url('/fonts/PPEiko-Thin.otf') format('opentype');
              font-weight: 300;
              font-style: normal;
              font-display: swap;
            }
            @font-face {
              font-family: 'PP Eiko';
              src: url('/fonts/PPEiko-Medium.otf') format('opentype');
              font-weight: 500;
              font-style: normal;
              font-display: swap;
            }
            @font-face {
              font-family: 'PP Eiko';
              src: url('/fonts/PPEiko-Heavy.otf') format('opentype');
              font-weight: 700;
              font-style: normal;
              font-display: swap;
            }
            .pp-eiko {
              font-family: 'PP Eiko', 'Manrope', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
              font-feature-settings: 'kern' 1, 'liga' 1;
            }
          `
        }} />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
