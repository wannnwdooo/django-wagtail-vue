import type { App } from "vue";

export function registerAllComponents(app: App<Element>): void {
  const componentsGlob: Record<string, any> = import.meta.glob('/src/components/**/*.vue', { eager: true });
  for (const path in componentsGlob) {
    const r = new RegExp('(\\/src\\/components\\/)([^\\/]+)\\/?(.*)(\\.vue)', 'g');
    const match = r.exec(path);
    if (match) {
      const fileName = match[3] ? match[3] : match[2];
      if (import.meta.env.NODE_ENV === 'development') {
        console.log('Component registered', fileName, path);
      }
      app.component(`v-${fileName}`, componentsGlob[path].default);
    }
  }
}

export function registerAllPages(app: App<Element>): void {
  const pagesGlob: Record<string, any> = import.meta.glob('/src/views/**/*.vue', { eager: true });
  for (const path in pagesGlob) {
    const r = new RegExp('(\\/src\\/views\\/)([^\\/]+)\\/?(.*)(\\.vue)', 'g');
    const match = r.exec(path);
    if (match) {
      const fileName = match[3] ? match[3] : match[2];
      if (import.meta.env.NODE_ENV === 'development') {
        console.log('Page registered', fileName, path);
      }
      app.component(`v-${fileName}`, pagesGlob[path].default);
    }
  }
}

export function registerAllDirectives(app: App<Element>): void {
  const directivesGlob: Record<string, any> = import.meta.glob('/src/directives/*.ts', { eager: true });
  for (const path in directivesGlob) {
    const r = new RegExp('(\\/src\\/directives\\/)([^\\/]+)\\/?(.*)(\\.ts)', 'g');
    const match = r.exec(path);
    if (match) {
      const directiveName = match[2];
      app.directive(directiveName, directivesGlob[path].default);
    }
  }
}