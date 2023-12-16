## Building

To create a production version of your app:

```bash
npm run build
```

### SvelteKit + NGINX
#### npm build시 build폴더와 index.html 생기게하기
```javascript
import adapter from '@sveltejs/adapter-static';
```
svelte.config.js 에서 adapter-auto 를 adapter-static으로 수정
