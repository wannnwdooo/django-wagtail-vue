## RU

Краткая документация по взаимодействию Vue с Wagtail/Django

Первым делом переходим в категорию vue внутри проекта и устанавливаем зависимости для vue

```bash
$ cd vue
$ npm i
```

Дальше выходим обратно в корневую директорию

```bash
$ cd ..
```

Стартуем приложение с помощью

```bash
$ sudo docker compose up --build
```

или

```bash
$ sudo docker-compose up --build
```

в зависимости какой compose у вас установлен

Заходим на http://localhost:8000

Одна из особенностей разработки заключается в том что для разработки нам не придется заходить на порт где стартует Vue,
а разрабатывать на порту Wagtail/Django.

У нас всё так же есть хот-релоад и другие фишки.

Фронтендеров в проекте будет интересовать только папки home(пускай даже это папка Wagtail), Vue и media/assets,
в последнеей будут храниться все статичные изображения.

Так как это MPA, а значит не типично для Vue разработчиков то накладывает некоторые ограничения.

Изображения мы сохраняем в директории описанной выше(media/assets),
путь/src к ним теперь нужно указывать в виде 'baseUrl + путь', пример вынесен в отдельный компонент.

После создании новой страницы в админке Wagtail нам следует создать шаблон в директории home/templates/home/название_шаблона.

Далее создаём страницу, она будет базовой для дочерних ей.

Эти дочерние страницы, мы описываем как динамические в router.

Что это даёт нам? Мы не смешиваем компоненты vue и шаблоны Wagtail/Django, 
не разбираемся в другом синтаксисе, не прокидываем пропсы из шаблона и не занимаемся deep props drilling, 
а просто работаем с api через сервисы и можем использовать стейт менеджер.

То есть MPA это все базовые страницы, но они являются SPA для всех дочерних.

Есть особенность с дочерними страницами, на них отображается контент основной.
Чтобы это исправить нам нужно на основных стораницах делать проверку url на то является ли страница базовой.
Посмотреть пример можно на основе страницы блога.

Так же при создании новой основной страницы блога, нужно создать соответствующий шаблон.
Зайдите в папку home/template/home и создайте там страницу по образу blog_page или home_page.

Вы можете создать дочерние страницы наведя указатель на основную и выбрав "Добавить дочернюю страницу".
Дальнейшие настройки вы должны проводить через сервис(пример blog.service) и router.

## EN

Brief documentation on how Vue interacts with Wagtail/Django

First of all, go to the vue category inside the project and install the dependencies for vue

```bash
$ cd vue
$ npm i
```

Then we go back to the root directory

```bash
$cd..
```

We start the application with

```bash
$ sudo docker compose up --build
```

or

```bash
$ sudo docker-compose up --build
```

depending on which compose you have installed

Go to http://localhost:8000

One of the development features is that for development we don’t have to go to the port where Vue starts,
and develop on the Wagtail/Django port.

We still have a hot reload and other features.

Frontend in the project will only be interested in the home folders (even if it is the Wagtail folder), Vue and media / assets,
the latter will store all static images.

Since this is an MPA, and therefore not typical for Vue developers, it imposes some restrictions.

We save images in the directory described above (media/assets),
the path/src to them now needs to be specified as 'baseUrl + path', the example is moved to a separate component.

After creating a new page in the Wagtail admin, we need to create a template in the home/templates/home/template_name directory.

Next, we create a page, it will be the base for its children.

These child pages, we describe as dynamic in router.

What does this give us? We don't mix vue components and Wagtail/Django templates,
we don’t understand other syntax, we don’t send props from the template, and we don’t do deep props drilling,
but we just work with api through services, and we can use the state manager.

That is, MPA are all base pages, but they are SPA for all child pages.

There is a feature with child pages, they display the main content.
To fix this, we need to check the url on the main pages to see if the page is the base one.
You can see an example based on the blog page.

Also, when creating a new main blog page, you need to create an appropriate template.
Go to the home/template/home folder and create a page in their like blog_page or home_page.

You can create child pages by hovering over the main page and selecting "Add Child Page".
Further settings you must carry out through the service (example blog.service) and router.