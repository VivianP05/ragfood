import { config } from '@tailwindcss/postcss';

export default {
  plugins: {
    '@tailwindcss/postcss': config('./tailwind.config.ts'),
  },
};
