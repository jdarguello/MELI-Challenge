import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/MELI-Challenge/__docusaurus/debug',
    component: ComponentCreator('/MELI-Challenge/__docusaurus/debug', 'fed'),
    exact: true
  },
  {
    path: '/MELI-Challenge/__docusaurus/debug/config',
    component: ComponentCreator('/MELI-Challenge/__docusaurus/debug/config', '1ed'),
    exact: true
  },
  {
    path: '/MELI-Challenge/__docusaurus/debug/content',
    component: ComponentCreator('/MELI-Challenge/__docusaurus/debug/content', '7ca'),
    exact: true
  },
  {
    path: '/MELI-Challenge/__docusaurus/debug/globalData',
    component: ComponentCreator('/MELI-Challenge/__docusaurus/debug/globalData', 'f4d'),
    exact: true
  },
  {
    path: '/MELI-Challenge/__docusaurus/debug/metadata',
    component: ComponentCreator('/MELI-Challenge/__docusaurus/debug/metadata', '79b'),
    exact: true
  },
  {
    path: '/MELI-Challenge/__docusaurus/debug/registry',
    component: ComponentCreator('/MELI-Challenge/__docusaurus/debug/registry', '249'),
    exact: true
  },
  {
    path: '/MELI-Challenge/__docusaurus/debug/routes',
    component: ComponentCreator('/MELI-Challenge/__docusaurus/debug/routes', '1d0'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog',
    component: ComponentCreator('/MELI-Challenge/blog', '934'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/archive',
    component: ComponentCreator('/MELI-Challenge/blog/archive', '0db'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/authors',
    component: ComponentCreator('/MELI-Challenge/blog/authors', 'df0'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/MELI-Challenge/blog/authors/all-sebastien-lorber-articles', '01e'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/authors/yangshun',
    component: ComponentCreator('/MELI-Challenge/blog/authors/yangshun', 'f1d'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/first-blog-post',
    component: ComponentCreator('/MELI-Challenge/blog/first-blog-post', '82f'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/long-blog-post',
    component: ComponentCreator('/MELI-Challenge/blog/long-blog-post', 'c30'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/mdx-blog-post',
    component: ComponentCreator('/MELI-Challenge/blog/mdx-blog-post', '532'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/tags',
    component: ComponentCreator('/MELI-Challenge/blog/tags', '00b'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/tags/docusaurus',
    component: ComponentCreator('/MELI-Challenge/blog/tags/docusaurus', 'd93'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/tags/facebook',
    component: ComponentCreator('/MELI-Challenge/blog/tags/facebook', '42b'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/tags/hello',
    component: ComponentCreator('/MELI-Challenge/blog/tags/hello', 'c97'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/tags/hola',
    component: ComponentCreator('/MELI-Challenge/blog/tags/hola', '807'),
    exact: true
  },
  {
    path: '/MELI-Challenge/blog/welcome',
    component: ComponentCreator('/MELI-Challenge/blog/welcome', '8ba'),
    exact: true
  },
  {
    path: '/MELI-Challenge/markdown-page',
    component: ComponentCreator('/MELI-Challenge/markdown-page', '99a'),
    exact: true
  },
  {
    path: '/MELI-Challenge/docs',
    component: ComponentCreator('/MELI-Challenge/docs', '14b'),
    routes: [
      {
        path: '/MELI-Challenge/docs',
        component: ComponentCreator('/MELI-Challenge/docs', '958'),
        routes: [
          {
            path: '/MELI-Challenge/docs',
            component: ComponentCreator('/MELI-Challenge/docs', '4c7'),
            routes: [
              {
                path: '/MELI-Challenge/docs/category/arquitectura-de-software',
                component: ComponentCreator('/MELI-Challenge/docs/category/arquitectura-de-software', '1a6'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/category/pruebas-automatizadas',
                component: ComponentCreator('/MELI-Challenge/docs/category/pruebas-automatizadas', '0fe'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/category/seguridad',
                component: ComponentCreator('/MELI-Challenge/docs/category/seguridad', '9b0'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/category/tutorial---extras',
                component: ComponentCreator('/MELI-Challenge/docs/category/tutorial---extras', '295'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/cloud/intro',
                component: ComponentCreator('/MELI-Challenge/docs/cloud/intro', '1b7'),
                exact: true,
                sidebar: "cloudSidebar"
              },
              {
                path: '/MELI-Challenge/docs/sdlc/arquitectura/generalidades',
                component: ComponentCreator('/MELI-Challenge/docs/sdlc/arquitectura/generalidades', '3c6'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/sdlc/arquitectura/oauth',
                component: ComponentCreator('/MELI-Challenge/docs/sdlc/arquitectura/oauth', '2f6'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/sdlc/calidad/frameworks',
                component: ComponentCreator('/MELI-Challenge/docs/sdlc/calidad/frameworks', '751'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/sdlc/calidad/introduccion',
                component: ComponentCreator('/MELI-Challenge/docs/sdlc/calidad/introduccion', '26a'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/sdlc/intro',
                component: ComponentCreator('/MELI-Challenge/docs/sdlc/intro', 'b8f'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/sdlc/seguridad/intro',
                component: ComponentCreator('/MELI-Challenge/docs/sdlc/seguridad/intro', '40a'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/sdlc/seguridad/vulns',
                component: ComponentCreator('/MELI-Challenge/docs/sdlc/seguridad/vulns', '45d'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/sdlc/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/MELI-Challenge/docs/sdlc/tutorial-extras/manage-docs-versions', '884'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/sdlc/tutorial-extras/translate-your-site',
                component: ComponentCreator('/MELI-Challenge/docs/sdlc/tutorial-extras/translate-your-site', 'e20'),
                exact: true,
                sidebar: "sdlcSidebar"
              },
              {
                path: '/MELI-Challenge/docs/supply-chain/',
                component: ComponentCreator('/MELI-Challenge/docs/supply-chain/', '24f'),
                exact: true,
                sidebar: "supplySidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/MELI-Challenge/',
    component: ComponentCreator('/MELI-Challenge/', '6cf'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
