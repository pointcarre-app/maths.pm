<!DOCTYPE html>
<html lang="en" data-theme="light">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>
      
        Maths.pm - Logiciels libres pour les enseignants de mathématiques
      
    </title>
    <link rel="icon" type="image/x-icon" href="../../../static/favicon/apple-icon-57x57.png" />

    
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@300..700&family=Cormorant+Garamond:ital,wght@0,300..700;1,300..700&family=Dancing+Script:wght@400..700&family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Lora:ital,wght@0,400..700;1,400..700&family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Source+Serif+4:ital,opsz,wght@0,8..60,200..900;1,8..60,200..900&family=Spectral:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,200;1,300;1,400;1,500;1,600;1,700;1,800&display=swap"
      rel="stylesheet" />



<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap"
      rel="stylesheet" />


<script>
    // Suppress Tailwind production warning for development
    window.process = {
        env: {
            NODE_ENV: 'development'
        }
    };
</script>
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
<link href="https://cdn.jsdelivr.net/npm/daisyui@5/themes.css" rel="stylesheet" type="text/css" />



<link rel="stylesheet" href="../../../static/css/root.css" />
<link rel="stylesheet" href="../../../static/css/styles.css" />
<link rel="stylesheet" href="../../../static/css/styles-alt.css" />



<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css" />
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<script>
    document.addEventListener("DOMContentLoaded", function() {
        if (typeof renderMathInElement !== 'undefined') {
            renderMathInElement(document.body, {
                delimiters: [{
                    left: '$$',
                    right: '$$',
                    display: true
                }, {
                    left: '$',
                    right: '$',
                    display: false
                }],
                throwOnError: false
            });
        } else {
            // Retry after a short delay if KaTeX isn't loaded yet
            setTimeout(function() {
                if (typeof renderMathInElement !== 'undefined') {
                    renderMathInElement(document.body, {
                        delimiters: [{
                            left: '$$',
                            right: '$$',
                            display: true
                        }, {
                            left: '$',
                            right: '$',
                            display: false
                        }],
                        throwOnError: false
                    });
                }
            }, 500);
        }
    });
</script>

    <meta name="description" content="Plateforme d&#39;enseignement des mathématiques pour le secondaire avec des cours interactifs, exercices et ressources pédagogiques libres. Aucune donnée collectée." />
    <meta name="keywords" content="mathématiques, enseignement, collège, lycée, cours, exercices, pédagogie, open source" />
    <meta name="author" content="Maths.pm, contact@pointcarre.app" />

    <!-- Custom head elements from domain config -->
    
      

      
    

    <!-- 🎯 Smart Product Dependency Loader -->
    
    

    
      
        
      
        
      
        
      
        
      
        
      
        
      
        
      
        
      
        
      
    

    <script>
        // Set backend settings as a global JS object
        // ... existing code ...
    </script>

    
  <meta charset="UTF-8" />
  <title>Maths Pedagogical Message</title>
  <meta name="description" content="Delivering pedagogical messages from Pointcarre.app" />
  <link rel="stylesheet" href="../../../static/core/css/pm.css" />
  <link rel="stylesheet" href="../../../static/core/css/toc.css" />
  <!-- MathLive for LaTeX (if needed later) -->
  <script src="https://cdn.jsdelivr.net/npm/mathlive@0.105.2/mathlive.min.js"></script>
  <link href="https://cdn.jsdelivr.net/npm/mathlive@0.105.2/mathlive-static.min.css" rel="stylesheet" />
  <!-- CodeMirror (for codex_ rendering) -->
  <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css" />
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/python/python.min.js"></script>
  <!-- Import map for JS namespace aliases -->
  <script type="importmap">
      {
          "imports": {
              "@js/": "/static/js/"
          }
      }
  </script>


  


  </head>

  <section class="fixed inset-0 w-screen h-screen z-[-10] overflow-hidden">


  <!-- <a href="http://127.0.0.1:8000/" class="flex items-center gap-1 sm:gap-2 bg-transparent pl-4 pt-3" style="position:absolute; top:0; left:0">
    <p class="w-8 h-8"><svg color="black" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 82 82">
  <g transform="translate(0,0)">
  <rect class="stroke-primary" x="5" y="5" width="72" height="72"  fill="transparent" stroke-width="10" rx="4" ry="4" stroke-linejoin="" />
  <rect class="stroke-primary fill-primary" x="36" y="36" width="10" height="10"   stroke-width="8" rx="1" ry="1" stroke-linejoin="" />
  </g>
</svg></p>
    <p class="font-heading">
      <span class="text-lg"><span class="">pointcarre</span>.app</span>
      
      
       
    </p>
</a> -->


  <svg xmlns="http://www.w3.org/2000/svg"
       viewBox="0 0 800 600"
       preserveAspectRatio="xMidYMid slice"
       width="100%"
       height="100%">
    <defs>
    <radialGradient id="gradient" cx="18%" cy="35%" r="15%" fx="18%" fy="35%">
    <stop offset="0%" stop-color="#a46dff" stop-opacity="0.5" />
    <stop offset="70%" stop-color="#a46dff" stop-opacity="0.3" />
    <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </radialGradient>

    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur in="SourceGraphic" stdDeviation="30" />
    </filter>

    
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#f0f0f0" stroke-width="0.5" />
    </pattern>

    
    <pattern id="notebook-lines" width="30" height="30" patternUnits="userSpaceOnUse">
    <!-- Main line (thicker) -->
    <line x1="0" y1="29" x2="30" y2="29" stroke="var(--color-primary)" stroke-width="0.35" opacity="0.10" />

    
    <line x1="0" y1="7" x2="30" y2="7" stroke="var(--color-primary)" stroke-width="0.45" opacity="0.10" />
    <line x1="0" y1="14" x2="30" y2="14" stroke="var(--color-primary)" stroke-width="0.35" opacity="0.10" />
    <line x1="0" y1="21" x2="30" y2="21" stroke="var(--color-primary)" stroke-width="0.35" opacity="0.10" />

    
    <line x1="29" y1="0" x2="29" y2="64" stroke="var(--color-primary)" stroke-width="0.45" opacity="0.10" />
    </pattern>
    </defs>

    
    <rect width="100%" height="100%" opacity="0.3" fill="var(--color-base-100)" />

    
    <rect width="100%" height="100%" fill="url(#notebook-lines)" opacity="0.5" />

    
    <!-- <line class="special-vertical-line" x1="149.5" y1="0" x2="149.5" y2="600" stroke="#FF007F" stroke-width="1" opacity="0" /> -->

    
    
  </svg>

</section>
  <body class="text-base-content font-sans min-h-screen">
    <data-brick>
  <div id="domain-config" 
       data-domain_yaml_path="domains/maths-pm.yml" 
       data-domain_url="https://maths.pm"
       
         data-domain_specific_metatags.viewport="width=device-width, initial-scale=1.0"
       
         data-domain_specific_metatags.theme-color="#FFFFFF"
       
         data-domain_specific_metatags.charset="UTF-8"
       
         data-domain_specific_metatags.subject="Enseignement des mathématiques et logiciels libres (Open Source)"
       
         data-domain_specific_metatags.copyright="SAS POINTCARRE.APP"
       
         data-domain_specific_metatags.language="FR"
       
         data-domain_specific_metatags.Classification="Education"
       
         data-domain_specific_metatags.author="Maths.pm, contact@pointcarre.app"
       
         data-domain_specific_metatags.designer="SAS POINTCARRE.APP"
       
         data-domain_specific_metatags.reply-to="contact@pointcarre.app"
       
         data-domain_specific_metatags.owner="SAS POINTCARRE.APP"
       
         data-domain_specific_metatags.directory="education"
       
         data-domain_specific_metatags.coverage="Europe"
       
         data-domain_specific_metatags.distribution="Europe"
       
         data-domain_specific_metatags.rating="General"
       
         data-domain_specific_metatags.revisit-after="7 days"
       
         data-domain_specific_metatags.target="all"
       
         data-domain_specific_metatags.HandheldFriendly="True"
       
         data-domain_specific_metatags.MobileOptimized="320"
       
         data-domain_specific_metatags.mobile-web-app-capable="yes"
       
         data-domain_specific_metatags.apple-mobile-web-app-capable="yes"
       
         data-domain_specific_metatags.apple-touch-fullscreen="yes"
       
         data-domain_specific_metatags.apple-mobile-web-app-status-bar-style="black"
       
         data-domain_specific_metatags.format-detection="telephone=no"
       
         data-domain_specific_metatags.medium="website"
       
         data-domain_specific_metatags.syndication-source="https://maths.pm"
       
         data-domain_specific_metatags.original-source="https://maths.pm"
       
         data-domain_specific_metatags.http-equiv-Expires="0"
       
         data-domain_specific_metatags.http-equiv-Pragma="no-cache"
       
         data-domain_specific_metatags.http-equiv-Cache-Control="no-cache"
       
         data-domain_specific_metatags.http-equiv-imagetoolbar="no"
       
         data-domain_specific_metatags.http-equiv-x-dns-prefetch-control="off"
       
         data-domain_specific_metatags.og:site_name="Maths.pm"
       
         data-domain_specific_metatags.og:email="contact@pointcarre.app"
       
         data-domain_specific_metatags.og:latitude="48.8566"
       
         data-domain_specific_metatags.og:longitude="2.3522"
       
         data-domain_specific_metatags.og:street-address="Your Address"
       
         data-domain_specific_metatags.og:locality="Paris"
       
         data-domain_specific_metatags.og:region="Île-de-France"
       
         data-domain_specific_metatags.og:postal-code="75001"
       
         data-domain_specific_metatags.og:country-name="France"
       
         data-domain_specific_metatags.twitter:site="@mathspm"
       
         data-domain_specific_metatags.twitter:site_name="Maths.pm"
       
         data-domain_specific_metatags.ICBM="48.8566, 2.3522"
       
         data-domain_specific_metatags.geo.region="FR-IDF"
       
         data-domain_specific_metatags.geo.placename="Paris"
       
         data-domain_specific_metatags.generator="HTML5"
       
         data-domain_specific_metatags.ResourceLoaderDynamicStyles=""
       
       
         data-index_view_specific_metatags.title="Maths.pm - Logiciels libres pour les enseignants de mathématiques"
       
         data-index_view_specific_metatags.description="Plateforme d&#39;enseignement des mathématiques pour le secondaire avec des cours interactifs, exercices et ressources pédagogiques libres. Aucune donnée collectée."
       
         data-index_view_specific_metatags.keywords="mathématiques, enseignement, collège, lycée, cours, exercices, pédagogie, open source"
       
         data-index_view_specific_metatags.robots="index, follow"
       
         data-index_view_specific_metatags.googlebot="index, follow"
       
         data-index_view_specific_metatags.revised="Jul. 17, 2025, 10:00 am"
       
         data-index_view_specific_metatags.abstract="Plateforme éducative pour l&#39;enseignement des mathématiques avec génération automatique d&#39;exercices et de sujets d&#39;examen."
       
         data-index_view_specific_metatags.topic="Enseignement des mathématiques"
       
         data-index_view_specific_metatags.summary="Ressources pédagogiques mathématiques pour professeurs : exercices, sujets d&#39;examen et outils Open Source."
       
         data-index_view_specific_metatags.url="https://maths.pm/"
       
         data-index_view_specific_metatags.identifier-URL="https://maths.pm/"
       
         data-index_view_specific_metatags.pagename="Accueil - Ressources mathématiques"
       
         data-index_view_specific_metatags.category="Education"
       
         data-index_view_specific_metatags.date="Jul. 17, 2025"
       
         data-index_view_specific_metatags.search_date="2025-07-17"
       
         data-index_view_specific_metatags.subtitle="Ressources pédagogiques mathématiques Open Source"
       
         data-index_view_specific_metatags.pageKey="maths-pm-home"
       
         data-index_view_specific_metatags.DC.title="Maths.pm - Ressources pédagogiques mathématiques Open Source"
       
         data-index_view_specific_metatags.DC.creator="Maths.pm, contact@pointcarre.app"
       
         data-index_view_specific_metatags.DC.subject="Enseignement, Mathématiques, Pédagogie, Open Source"
       
         data-index_view_specific_metatags.itemprop-name="Maths.pm - Ressources mathématiques"
       
         data-index_view_specific_metatags.og:title="Maths.pm - Ressources pédagogiques mathématiques"
       
         data-index_view_specific_metatags.og:description="Plateforme éducative pour professeurs de mathématiques. Exercices et sujets générés automatiquement avec des technologies Open Source."
       
         data-index_view_specific_metatags.og:image="https://maths.pm/static/images/maths-pm-social-card.jpg"
       
         data-index_view_specific_metatags.og:type="website"
       
         data-index_view_specific_metatags.og:url="https://maths.pm/"
       
         data-index_view_specific_metatags.twitter:card="summary_large_image"
       
         data-index_view_specific_metatags.twitter:creator="@mathspm"
       
         data-index_view_specific_metatags.twitter:title="Maths.pm - Ressources pédagogiques mathématiques"
       
         data-index_view_specific_metatags.twitter:description="Plateforme éducative pour professeurs de mathématiques. Exercices et sujets générés automatiquement."
       
         data-index_view_specific_metatags.twitter:image="https://maths.pm/static/images/maths-pm-twitter-card.jpg"
       
         data-index_view_specific_metatags.twitter:image:alt="Logo Maths.pm avec formules mathématiques"
       
         data-index_view_specific_metatags.twitter:url="https://maths.pm/"
       
       
         data-extra_head.js="[]"
       
         data-extra_head.css="[]"
       
       
         data-templating.base_template="base/main-alt.html"
       
         data-templating.footer_template="domains/maths-pm/footers.html"
       
         data-templating.navbar_title="Maths.pm"
       
         data-templating.button_primary_text="Ressources"
       
         data-templating.button_primary_href="/"
       
         data-templating.button_ghost_text="Contact"
       
         data-templating.button_ghost_href="/contact"
       >
  </div>

  <div id="backend-public-settings"
       
         data-nagini="{&#34;endpoint&#34;: &#34;https://cdn.jsdelivr.net/gh/your-org/nagini@0.0.17/&#34;, &#34;js_url&#34;: &#34;https://cdn.jsdelivr.net/gh/your-org/nagini@0.0.17/src/nagini.js&#34;, &#34;pyodide_worker_url&#34;: &#34;https://cdn.jsdelivr.net/gh/your-org/nagini@0.0.17/src/pyodide/worker/worker-dist.js&#34;}"
       
         data-v4pyjs="{&#34;lib_url&#34;: &#34;https://cdn.jsdelivr.net/gh/your-org/v4.py.js@v0.0.4-unstable/&#34;}"
       
         data-teachers="{&#34;endpoint&#34;: &#34;https://cdn.jsdelivr.net/gh/your-org/teachers@0.0.2/&#34;, &#34;files_to_load&#34;: [{&#34;url&#34;: &#34;https://cdn.jsdelivr.net/gh/your-org/teachers@0.0.2/src/teachers/__init__.py&#34;, &#34;path&#34;: &#34;teachers/__init__.py&#34;}, {&#34;url&#34;: &#34;https://cdn.jsdelivr.net/gh/your-org/teachers@0.0.2/src/teachers/generator.py&#34;, &#34;path&#34;: &#34;teachers/generator.py&#34;}, {&#34;url&#34;: &#34;https://cdn.jsdelivr.net/gh/your-org/teachers@0.0.2/src/teachers/maths.py&#34;, &#34;path&#34;: &#34;teachers/maths.py&#34;}, {&#34;url&#34;: &#34;https://cdn.jsdelivr.net/gh/your-org/teachers@0.0.2/src/teachers/formatting.py&#34;, &#34;path&#34;: &#34;teachers/formatting.py&#34;}, {&#34;url&#34;: &#34;https://cdn.jsdelivr.net/gh/your-org/teachers@0.0.2/src/teachers/corrector.py&#34;, &#34;path&#34;: &#34;teachers/corrector.py&#34;}, {&#34;url&#34;: &#34;https://cdn.jsdelivr.net/gh/your-org/teachers@0.0.2/src/teachers/defaults.py&#34;, &#34;path&#34;: &#34;teachers/defaults.py&#34;}]}"
       
         data-arpege_generator_script_paths="[&#34;/static/py/services/sujets0/spe_sujet1_auto_01_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet1_auto_02_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet1_auto_03_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet1_auto_04_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet1_auto_05_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet1_auto_06_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet1_auto_07_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet1_auto_08_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet1_auto_09_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet1_auto_10_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet1_auto_11_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet1_auto_12_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet2_auto_01_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet2_auto_02_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet2_auto_03_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet2_auto_04_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet2_auto_05_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet2_auto_06_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet2_auto_07_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet2_auto_08_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet2_auto_09_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet2_auto_10_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet2_auto_11_question.py&#34;, &#34;/static/py/services/sujets0/spe_sujet2_auto_12_question.py&#34;]"
       
         data-corpus=""
       
         data-jupyterlite="{&#34;enabled&#34;: &#34;true&#34;, &#34;version&#34;: &#34;0.4.3&#34;, &#34;kernels&#34;: [&#34;python&#34;], &#34;packages&#34;: [&#34;numpy&#34;, &#34;matplotlib&#34;, &#34;sympy&#34;], &#34;pyodide&#34;: {&#34;version&#34;: &#34;0.26.4&#34;, &#34;packages&#34;: [&#34;micropip&#34;, &#34;numpy&#34;, &#34;matplotlib&#34;]}}"
       
         data-examples="{&#34;enabled&#34;: &#34;true&#34;, &#34;description&#34;: &#34;Test and example files for PM features&#34;}"
       >
  </div>

  <div id="nagini-settings" data-endpoint="">
  </div>

  <div id="pca-corpus-settings"
       data-endpoint=""
       data-paths-to-load="[]">
  </div>

  <div id="pca-teachers-settings"
       data-endpoint=""
       data-paths-to-load="[]">
  </div>

  <div id="pronoia-sujets-0-qcm-config" 
       data-partie="1" 
       data-partie-rdb="Automatismes" 
       data-generation-mode="maths">
  </div>
</data-brick>

    <div class="navbar main-alt-navbar bg-base-100">
  <div class="navbar-start">
    <a href="https://maths.pm" class="w-[32px] sm:w-[40px] h-[32px] sm:h-[40px]">
      <svg color="black" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 82 82">
  <g transform="translate(0,0)">
  <rect class="stroke-primary" x="5" y="5" width="72" height="72"  fill="transparent" stroke-width="10" rx="4" ry="4" stroke-linejoin="" />
  <rect class="stroke-primary fill-primary" x="36" y="36" width="10" height="10"   stroke-width="8" rx="1" ry="1" stroke-linejoin="" />
  </g>
</svg>
    </a>
    <!-- Mobile title shown next to logo on small screens -->
    <a href="/" class="navbar-alt-title-mobile">Maths.pm</a>
  </div>
  <div class="navbar-center">
    <div class="text-2xl sm:text-3xl">
      
        <a href="/" class="font-handwritten">Maths.pm</a>
      
    </div>
  </div>
  <div class="navbar-end gap-2 sm:pl-18">
    <button class="btn btn-sm sm:btn-base btn-square btn-ghost"
            onclick="my_modal_1.showModal()"
            style="box-shadow: none !important;
                   border: none !important;
                   font-weight:400">
      <svg xmlns="http://www.w3.org/2000/svg"
           width="20"
           height="20"
           viewBox="0 0 24 24"
           fill="none"
           stroke="currentColor"
           stroke-width="2"
           stroke-linecap="round"
           stroke-linejoin="round"
           class="lucide lucide-book-type-icon lucide-book-type">
        <path d="M10 13h4" />
        <path d="M12 6v7" />
        <path d="M16 8V6H8v2" />
        <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20" />
      </svg>
    </button>
    <dialog id="my_modal_1" class="modal">
      <div class="modal-box"><div class="py-8 sm:px-6">
  <div class="text-left mb-8">
    <h2 class="text-2xl font-bold mb-2">Licences et droits d'usage</h2>
  </div>

  <div class="bg-base-100 rounded-lg border border-base-300 p-2 sm:p-6 mb-6">
    <div class="max-w-3xl mx-auto">
  <div class="flex flex-col sm:flex-row w-full py-2">
    <div class="grid grow place-items-center sm:h-30">
      <div class="flex flex-col items-center">
        <div class="text-sm sm:text-base text-center font-heading mb-2">Codes sources</div>
        <img class="h-[40px]" src="../../../static/icons/AGPLv3_Logo.svg" alt="Logo licence AGPLv3">
      </div>
    </div>
    <div class="divider divider-horizontal text-xs px-12">
      <span class="hidden sm:block"><span class="badge badge-sm badge-primary">LICENCES</span></span>
    </div>
    <div class="grid grow place-items-center sm:h-30">
      <div class="flex flex-col">
        <div class="text-sm sm:text-base text-center font-heading mb-2">Contenus</div>
        <img class="h-[40px]" src="../../../static/icons/CC_BY-NC-SA.svg" alt="Logo licence Creative Commons">
      </div>
    </div>
  </div>
</div> 
  </div>


  <details class="p-0">
    <summary class="cursor-pointer  hover:bg-base-100 rounded-lg text-sm">
      <span class="select-none">Codes sources : AGPLv3</span>
    </summary>
    <div class="px-4 pb-4 pt-4 text-sm leading-relaxed">
      <div class="flex justify-center mb-4">
        <img class="w-24 h-auto"
             src="../../../static/icons/licenses/AGPLv3_Logo.svg"
             alt="Logo licence AGPLv3"
             width="96"
             height="96" />
      </div>
      <p>
        Tous les codes sources des ressources référencées sur ce site et créées par la SAS Pointcarre.app sont distribués sous licence
        <a href="https://www.gnu.org/licenses/agpl-3.0.html" target="_blank" class="link link-primary">AGPLv3</a>.
      </p>
      <p class="mt-2">
        Vous êtes libre de les utiliser, modifier et redistribuer, y compris pour un usage commercial,
        à condition de partager vos modifications sous la même licence.
      </p>
    </div>
  </details>

  <details class="p-0">
    <summary class="cursor-pointer  hover:bg-base-100 rounded-lg text-sm">
      <span class="select-none">Contenus : CC BY-NC-SA 4.0</span>
    </summary>
    <div class="px-4 pb-4 pt-4 text-sm leading-relaxed">
      <div class="flex justify-center mb-4">
        <img class="w-24 h-auto"
             src="../../../static/icons/licenses/CC_BY-NC-SA.svg"
             alt="Logo licence Creative Commons BY-NC-SA"
             width="96"
             height="96" />
      </div>
      <p>
        Tous les contenus référencés sur ce site et créés par la SAS Pointcarre.app
        (exercices, cours, articles, documentation, mentions légales, etc.) sont sous licence
        <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" class="link link-primary">CC BY-NC-SA 4.0</a>.
      </p>
      <p class="mt-2">
        Vous pouvez les partager et les adapter librement pour un usage non commercial,
        en citant la source et en conservant la même licence.
      </p>
    </div>
  </details>

  <div class="modal-action"></div>
  <div class="text-right">
    <form method="dialog">
      <button class="btn btn-soft">Fermer</button>
    </form>
  </div>


</div></div>
    </dialog>
    <a class="btn btn-sm sm:btn-base btn-square btn-ghost"
       style="box-shadow: none !important;
              border: none !important;
              font-weight:400">
      <svg xmlns="http://www.w3.org/2000/svg"
           width="20"
           height="20"
           viewBox="0 0 24 24"
           fill="none"
           stroke="currentColor"
           stroke-width="2"
           stroke-linecap="round"
           stroke-linejoin="round"
           class="lucide lucide-upload-icon lucide-upload">
        <path d="M12 3v12"></path>
        <path d="m17 8-5-5-5 5"></path>
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
      </svg>
    </a>
    <a href="/"
       class="btn btn-sm sm:btn-base btn-primary"
       style="padding: 0.5rem 0.75rem;
              box-shadow: none !important;
              font-weight:300">Ressources</a>
    <a href="/contact"
       class="btn btn-sm sm:btn-base btn-ghost"
       style="padding: 0.5rem 0.75rem;
              box-shadow: none !important;
              font-weight:300">Contact</a>
  </div>
</div>
    
    <style>
    @media (max-width: 639px) {
        #left-sidebar {
            border-right: none !important;
        }
    }
</style>

<!-- Toggle buttons -->
<style>
    @keyframes spin-then-scale {
        0% {
            transform: rotate(0deg) scale(1);
        }

        50% {
            transform: rotate(360deg) scale(1);
        }

        100% {
            transform: rotate(360deg) scale(1.2);
        }
    }

    .spin-scale-hover:hover {
        animation: spin-then-scale 1s ease-in-out forwards;
    }
</style>







<div class="fixed  right-0 top-0 h-screen w-[calc(250px+1rem)] bg-base-200/90 backdrop-blur text-base-content z-40 transition-transform duration-300 overflow-y-auto translate-x-full"
     id="right-sidebar">
  <ul class="menu p-4 min-h-full mt-12" style="width: 250px !important;">


    <li>


      <a href="/dashboard" class="flex justify-between items-center">


        
      </a>

    </li>

    <li>
      <a href="/doppel"
         class="flex justify-between items-center hover:bg-primary hover:text-primary-content"
         style="width: 100% !important;
                background-color: color-mix(in oklab, var(--color-secondary, var(--color-base-content)) 8%, var(--color-base-100))">
        <span>Data-brick</span>
        <svg xmlns="http://www.w3.org/2000/svg"
             width="18"
             height="18"
             viewBox="0 0 24 24"
             fill="none"
             stroke="currentColor"
             stroke-width="1.5"
             stroke-linecap="round"
             stroke-linejoin="round"
             class="lucide lucide-cuboid-icon lucide-cuboid">
          <path d="m21.12 6.4-6.05-4.06a2 2 0 0 0-2.17-.05L2.95 8.41a2 2 0 0 0-.95 1.7v5.82a2 2 0 0 0 .88 1.66l6.05 4.07a2 2 0 0 0 2.17.05l9.95-6.12a2 2 0 0 0 .95-1.7V8.06a2 2 0 0 0-.88-1.66Z" />
          <path d="M10 22v-8L2.25 9.15" />
          <path d="m10 14 11.77-6.87" />
        </svg>
      </a>
      <ul id="doppel-all-files-list" style="margin-left: 0rem !important;">
        <!-- All files will be populated here consecutively -->
      </ul>
    </li>

    <li>
      <a href="/doppel"
         class="flex justify-between items-center hover:bg-primary hover:text-primary-content"
         style="width: 100% !important;
                background-color: color-mix(in oklab, var(--color-secondary, var(--color-base-content)) 8%, var(--color-base-100))">
        <span>Doppel</span>
        <svg xmlns="http://www.w3.org/2000/svg"
             width="18"
             height="18"
             viewBox="0 0 24 24"
             fill="none"
             stroke="currentColor"
             stroke-width="1.5"
             stroke-linecap="round"
             stroke-linejoin="round"
             class="lucide lucide-drama-icon lucide-drama">
          <path d="M10 11h.01" />
          <path d="M14 6h.01" />
          <path d="M18 6h.01" />
          <path d="M6.5 13.1h.01" />
          <path d="M22 5c0 9-4 12-6 12s-6-3-6-12c0-2 2-3 6-3s6 1 6 3" />
          <path d="M17.4 9.9c-.8.8-2 .8-2.8 0" />
          <path d="M10.1 7.1C9 7.2 7.7 7.7 6 8.6c-3.5 2-4.7 3.9-3.7 5.6 4.5 7.8 9.5 8.4 11.2 7.4.9-.5 1.9-2.1 1.9-4.7" />
          <path d="M9.1 16.5c.3-1.1 1.4-1.7 2.4-1.4" />
        </svg>
      </a>
      <ul id="doppel-all-files-list" style="margin-left: 0rem !important;">
        <!-- All files will be populated here consecutively -->
      </ul>
    </li>

    <!-- Theme Selector - moved outside the main li to avoid overflow issues -->
    <li class="mt-6">
      <div class="text-sm font-semibold mb-2">Thèmes</div>
      <ul class="">
        <li>
          <button class="btn btn-sm bg-base-200/50 hover:bg-primary hover:text-primary-content w-full"
                  onclick="document.documentElement.setAttribute('data-theme', 'bolt')">
            ⚡️ Bolt
          </button>
        </li>
        <li>
          <button class="btn btn-sm bg-base-200/50 hover:bg-primary hover:text-primary-content w-full"
                  onclick="document.documentElement.setAttribute('data-theme', 'purple')">
            🟪 Purple
          </button>
        </li>
        <li>
          <button class="btn btn-sm bg-base-200/50 hover:bg-primary hover:text-primary-content w-full"
                  onclick="document.documentElement.setAttribute('data-theme', 'dark-black')">
            ⚫️ DarkBlack
          </button>
        </li>

        <li>
          <button class="btn btn-sm bg-base-200/50 hover:bg-primary hover:text-primary-content w-full"
                  onclick="document.documentElement.setAttribute('data-theme', 'night')">
            🌒 Night
          </button>
        </li>


        <li>
          <button class="btn btn-sm bg-base-200/50 hover:bg-primary hover:text-primary-content w-full"
                  onclick="document.documentElement.setAttribute('data-theme', 'light')">
            Light
          </button>
        </li>
        <li>
          <button class="btn btn-sm bg-base-200/50 hover:bg-primary hover:text-primary-content w-full"
                  onclick="document.documentElement.setAttribute('data-theme', 'dark')">
            Dark
          </button>
        </li>
        <li>
          <button class="btn btn-sm bg-base-200/50 hover:bg-primary hover:text-primary-content w-full"
                  onclick="document.documentElement.setAttribute('data-theme', 'zelie')">
            Zelie
          </button>
        </li>
        <li>
          <button class="btn btn-sm bg-base-200/50 hover:bg-primary hover:text-primary-content w-full"
                  onclick="document.documentElement.setAttribute('data-theme', 'cyberpunk')">
            Cyberpunk
          </button>
        </li>
        <li>
          <button class="btn btn-sm bg-base-200/50 hover:bg-primary hover:text-primary-content w-full"
                  onclick="document.documentElement.setAttribute('data-theme', 'dracula')">
            Dracula
          </button>
        </li>
        <li>
          <button class="btn btn-sm bg-base-200/50 hover:bg-primary hover:text-primary-content w-full"
                  onclick="document.documentElement.setAttribute('data-theme', 'emerald')">
            Emerald
          </button>
        </li>
        <li>
          <button class="btn btn-sm bg-base-200/50 hover:bg-primary hover:text-primary-content w-full"
                  onclick="document.documentElement.setAttribute('data-theme', 'nord')">
            Nord
          </button>
        </li>
      </ul>
    </li>

    <li class="mt-auto">
      <div class="join font-mono">
        <span class="badge join-item badge-neutral">1<sup>ère</sup></span>
        <span class="badge join-item badge-secondary badge-soft">Spé. Maths</span>
      </div>
    </li>
  </ul>


</div>


<button class="btn btn-circle hover:bg-transparent btn-lg fixed bottom-4 right-4 z-50 spin-scale-hover"
        id="right-toggle">
  <svg xmlns="http://www.w3.org/2000/svg"
       width="18"
       height="18"
       viewBox="0 0 24 24"
       fill="none"
       stroke="currentColor"
       stroke-width="1"
       stroke-linecap="round"
       stroke-linejoin="round">
    <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" />
    <circle cx="12" cy="12" r="3" />
  </svg>
</button>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        // Sidebar toggle
        const leftSidebar = document.getElementById('left-sidebar');
        const rightSidebar = document.getElementById('right-sidebar');
        const leftToggle = document.getElementById('left-toggle');
        const rightToggle = document.getElementById('right-toggle');

        try {

            leftToggle.addEventListener('click', () => {
                leftSidebar.classList.toggle('-translate-x-full');
            });
        } catch (e) {
            console.log("no leftsidebar found")
            console.error(e);
        }


        try {

            rightToggle.addEventListener('click', () => {
                rightSidebar.classList.toggle('translate-x-full');
            });
        } catch (e) {
            console.log("no rightsidebar found")
            console.error(e);
        }

        // Theme management
        function setTheme(theme) {
            document.documentElement.setAttribute("data-theme", theme);
            localStorage.setItem("theme", theme);
        }

        function initializeTheme() {
            const savedTheme = localStorage.getItem("theme");
            if (savedTheme) {
                setTheme(savedTheme);
            } else {
                const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
                setTheme(prefersDark ? "dark" : "light");
            }
        }

        initializeTheme();

        // Add event listeners to theme buttons - updated for new button structure
        const themeButtons = document.querySelectorAll("button[onclick*='data-theme']");
        themeButtons.forEach((button) => {
            const originalOnClick = button.getAttribute("onclick");
            button.removeAttribute("onclick");
            const themeMatch = originalOnClick.match(/data-theme', '([^']+)'/);
            const themeName = themeMatch ? themeMatch[1] : "light";
            button.addEventListener("click", function() {
                setTheme(themeName);
            });
        });

        // Listen for system theme changes
        window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
            if (!localStorage.getItem("theme")) {
                setTheme(e.matches ? "dark" : "light");
            }
        });
    });
</script>

    <main class="container mx-auto">
      
  <!-- djlint:off -->
                      

                      <div class="sidebar-fixed hidden xl:block">
                        <div class="w-72 flex flex-col card">
      <div id="toc" class="p-4 flex-none text-left text-base-content/80"></div>
    </div>
  </div>

  <div class="pm-container lg:text-lg w-full md:max-w-3xl lg:max-w-4xl xl:max-w-4xl mx-auto">
    <div class="bg-base-100 shadow-2xl mt-12 px-4 py-4">
      <!-- Main Content -->
      <div class="max-w-[640px] mx-auto md:py-12 bg-base-100">
        
          <div class="bg-warning text-warning-content text-center p-6 mb-12">
            NO PRODUCT SETTINGS FOUND FOR:
            <br />
            <div class="font-mono badge">documentation</div>
            <br />
            <div class="text-left text-xs">
              Gentle remainder that the product name comes from the `origin` first subfolder (after `/pms` ).
            </div>
          </div>
        

        <!-- Fragments (rendered via partials) -->
        
        
          
          
          
            
            
              
              <div class="fragment-wrapper " data-f_type="h1_">
                <h1 id="pm-system-documentation"
    class="fragment text-2xl sm:text-3xl md:text-4xl font-bold"
    data-f_type="h1_">📚 PM System Documentation</h1>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_">Welcome to the Pedagogical Message (PM) system documentation. This folder contains comprehensive guides and references for creating rich, interactive educational content.</p>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h2_">
                <h2 id="documentation-structure"
    class="fragment text-xl sm:text-2xl md:text-3xl font-semibold"
    data-f_type="h2_">📖 Documentation Structure</h2>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="quick-start"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">🎯 Quick Start</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ul_">
                <ul class="fragment" data-f_type="ul_">
  <ul class="">
<li><strong><a href="fragments_quick_reference.md">Fragments Quick Reference</a></strong> - One-page cheat sheet for all fragment types</li>
<li><strong><a href="all_fragments_showcase.md">All Fragments Showcase</a></strong> - Live examples of every fragment type</li>
</ul>
</ul>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="detailed-guides"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">📝 Detailed Guides</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h4_">
                <h4 id="text-structure"
    class="fragment text-lg font-medium"
    data-f_type="h4_">Text &amp; Structure</h4>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ul_">
                <ul class="fragment" data-f_type="ul_">
  <ul class="">
<li><strong><a href="text_fragments_guide.md">Text Fragments Guide</a></strong> - Complete guide to headings, paragraphs, lists, and text formatting</li>
</ul>
</ul>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h4_">
                <h4 id="interactivity"
    class="fragment text-lg font-medium"
    data-f_type="h4_">Interactivity</h4>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ul_">
                <ul class="fragment" data-f_type="ul_">
  <ul class="">
<li><strong><a href="interactive_fragments_guide.md">Interactive Fragments Guide</a></strong> - Radio buttons, math input, graphs, and interactive code</li>
<li><strong><a href="i_radio_fragment_guide.md">i-Radio Fragment Guide</a></strong> - Deep dive into the radio button system with flags</li>
</ul>
</ul>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h4_">
                <h4 id="media-code"
    class="fragment text-lg font-medium"
    data-f_type="h4_">Media &amp; Code</h4>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ul_">
                <ul class="fragment" data-f_type="ul_">
  <ul class="">
<li><strong><a href="code_media_fragments_guide.md">Code &amp; Media Fragments Guide</a></strong> - Code blocks, images, SVGs, and visualizations</li>
</ul>
</ul>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h2_">
                <h2 id="getting-started"
    class="fragment text-xl sm:text-2xl md:text-3xl font-semibold"
    data-f_type="h2_">🚀 Getting Started</h2>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="1-basic-pm-structure"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">1. Basic PM Structure</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_">Every PM file starts with YAML frontmatter:</p>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="code_">
                <div class="fragment mockup-code" data-f_type="code_">
  <pre class="fragment-code"><code class="language-yaml">---
title: Your PM Title
description: Brief description
chapter: Chapter Name
---
</code></pre>
</div>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="2-essential-fragments"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">2. Essential Fragments</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_">The most commonly used fragments:</p>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="code_">
                <div class="fragment mockup-code" data-f_type="code_">
  <pre class="fragment-code"><code class="language-markdown"># Main Title

Introduction paragraph with **emphasis**.
{: .lead}

## Section

Regular content goes here.

- Bullet point 1
- Bullet point 2

What&#39;s the answer?

- Wrong{:21}
- Correct{:20}
{: .i-radio}
</code></pre>
</div>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="3-adding-interactivity"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">3. Adding Interactivity</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_">Make your content engaging:</p>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="code_">
                <div class="fragment mockup-code" data-f_type="code_">
  <pre class="fragment-code"><code class="language-yaml">codexPCAVersion: 1
script_path: &#34;examples/hello.py&#34;
</code></pre>
</div>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h2_">
                <h2 id="fragment-categories"
    class="fragment text-xl sm:text-2xl md:text-3xl font-semibold"
    data-f_type="h2_">🎨 Fragment Categories</h2>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="core-fragments"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Core Fragments</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ul_">
                <ul class="fragment" data-f_type="ul_">
  <ul class="">
<li><strong>Text</strong>: h1_, h2_, h3_, h4_, p_, q_</li>
<li><strong>Lists</strong>: ul_, ol_, lbl_</li>
<li><strong>Structure</strong>: toc_, hr_</li>
</ul>
</ul>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="interactive-fragments"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Interactive Fragments</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ul_">
                <ul class="fragment" data-f_type="ul_">
  <ul class="">
<li><strong>radio_</strong>: Multiple choice questions</li>
<li><strong>maths_</strong>: Mathematical input</li>
<li><strong>graph_</strong>: Function plotting</li>
<li><strong>codex_</strong>: Executable code</li>
</ul>
</ul>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="media-fragments"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Media Fragments</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ul_">
                <ul class="fragment" data-f_type="ul_">
  <ul class="">
<li><strong>image_</strong>: Static images</li>
<li><strong>svg_</strong>: Vector graphics</li>
<li><strong>code_</strong>: Syntax-highlighted code</li>
</ul>
</ul>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="data-fragments"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Data Fragments</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ul_">
                <ul class="fragment" data-f_type="ul_">
  <ul class="">
<li><strong>table_</strong>: Data tables</li>
<li><strong>tabvar_</strong>: Variation tables</li>
</ul>
</ul>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h2_">
                <h2 id="advanced-features"
    class="fragment text-xl sm:text-2xl md:text-3xl font-semibold"
    data-f_type="h2_">🔧 Advanced Features</h2>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="styling-with-attributes"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Styling with Attributes</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="code_">
                <div class="fragment mockup-code" data-f_type="code_">
  <pre class="fragment-code"><code class="language-markdown">Important note here.
{: .lead .bg-primary .text-center}
</code></pre>
</div>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="combining-fragments"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Combining Fragments</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_">Mix different fragment types for rich content:
- Text explanation
- Visual diagram
- Interactive question
- Code example</p>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="custom-classes"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Custom Classes</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_">Apply CSS classes for precise control:
- <code>.mx-auto</code> - Center horizontally
- <code>.max-w-[size]</code> - Limit width
- <code>.bg-[color]</code> - Background colors
- <code>.text-[style]</code> - Text styling</p>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h2_">
                <h2 id="project-structure"
    class="fragment text-xl sm:text-2xl md:text-3xl font-semibold"
    data-f_type="h2_">📁 Project Structure</h2>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="code_">
                <div class="fragment mockup-code" data-f_type="code_">
  <pre class="fragment-code"><code class="language-python">pms/
├── documentation/     # You are here
│   ├── README.md     # This file
│   ├── fragments_quick_reference.md
│   ├── all_fragments_showcase.md
│   ├── text_fragments_guide.md
│   ├── interactive_fragments_guide.md
│   ├── code_media_fragments_guide.md
│   └── i_radio_fragment_guide.md
├── examples/         # Example PMs
│   └── i_radio_example.md
├── corsica/         # Corsica project
│   ├── a_troiz_geo.md
│   ├── e_seconde_stats_python.md
│   └── files/      # Project assets
└── pyly/           # Python lessons
    ├── 00_index.md
    ├── 01_premiers_pas.md
    └── files/      # Lesson assets
</code></pre>
</div>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h2_">
                <h2 id="best-practices"
    class="fragment text-xl sm:text-2xl md:text-3xl font-semibold"
    data-f_type="h2_">🎯 Best Practices</h2>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="content-organization"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Content Organization</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ol_">
                <ol class="fragment" data-f_type="ol_">
  <ol class="">
<li><strong>Clear hierarchy</strong> - Use headings consistently</li>
<li><strong>Logical flow</strong> - Build concepts progressively</li>
<li><strong>Visual breaks</strong> - Use dividers and spacing</li>
<li><strong>Consistent styling</strong> - Apply classes uniformly</li>
</ol>
</ol>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="interactivity"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Interactivity</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ol_">
                <ol class="fragment" data-f_type="ol_">
  <ol class="">
<li><strong>Immediate feedback</strong> - Use flags for radio buttons</li>
<li><strong>Clear instructions</strong> - Explain what users should do</li>
<li><strong>Progressive difficulty</strong> - Start simple, increase complexity</li>
<li><strong>Helpful hints</strong> - Add non-flagged hints in radio lists</li>
</ol>
</ol>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="performance"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Performance</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ol_">
                <ol class="fragment" data-f_type="ol_">
  <ol class="">
<li><strong>Optimize images</strong> - Compress and use appropriate formats</li>
<li><strong>Lazy loading</strong> - Large content loads on demand</li>
<li><strong>Code splitting</strong> - Break large examples into parts</li>
<li><strong>Caching</strong> - Leverage browser caching</li>
</ol>
</ol>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="accessibility"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Accessibility</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ol_">
                <ol class="fragment" data-f_type="ol_">
  <ol class="">
<li><strong>Alt text</strong> - Describe all images</li>
<li><strong>Semantic HTML</strong> - Use proper heading hierarchy</li>
<li><strong>Keyboard navigation</strong> - Ensure all interactive elements are accessible</li>
<li><strong>Contrast</strong> - Maintain readable color combinations</li>
</ol>
</ol>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h2_">
                <h2 id="fragment-processing-pipeline"
    class="fragment text-xl sm:text-2xl md:text-3xl font-semibold"
    data-f_type="h2_">🔍 Fragment Processing Pipeline</h2>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="code_">
                <div class="fragment mockup-code" data-f_type="code_">
  <pre class="fragment-code"><code class="language-mermaid">graph LR
    A[Markdown] --&amp;gt; B[Parse with Extensions]
    B --&amp;gt; C[HTML + Metadata]
    C --&amp;gt; D[Fragment Builder]
    D --&amp;gt; E[Fragment Objects]
    E --&amp;gt; F[Validation]
    F --&amp;gt; G[Template Rendering]
    G --&amp;gt; H[Final Output]
</code></pre>
</div>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h2_">
                <h2 id="tips-tricks"
    class="fragment text-xl sm:text-2xl md:text-3xl font-semibold"
    data-f_type="h2_">💡 Tips &amp; Tricks</h2>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="quick-testing"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Quick Testing</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_">Test fragments locally by creating a simple PM file and viewing it in the browser.</p>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="fragment-validation"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Fragment Validation</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_">The system validates fragment structure automatically - check console for errors.</p>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="custom-extensions"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Custom Extensions</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_">The markdown processor supports several extensions:
- <code>toc</code> - Table of contents
- <code>tables</code> - Enhanced tables
- <code>fenced_code</code> - Code blocks
- <code>attr_list</code> - Attribute lists <code>{: .class}</code>
- <code>full_yaml_metadata</code> - YAML frontmatter</p>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h3_">
                <h3 id="debugging"
    class="fragment text-lg sm:text-xl md:text-2xl font-medium"
    data-f_type="h3_">Debugging</h3>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_">Enable verbosity in PM builder for detailed processing information.</p>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h2_">
                <h2 id="learning-path"
    class="fragment text-xl sm:text-2xl md:text-3xl font-semibold"
    data-f_type="h2_">📚 Learning Path</h2>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="ol_">
                <ol class="fragment" data-f_type="ol_">
  <ol class="">
<li>Start with <strong><a href="fragments_quick_reference.md">Fragments Quick Reference</a></strong></li>
<li>Explore <strong><a href="all_fragments_showcase.md">All Fragments Showcase</a></strong></li>
<li>Read specific guides as needed</li>
<li>Create your own PM files</li>
<li>Test and iterate</li>
</ol>
</ol>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h2_">
                <h2 id="contributing"
    class="fragment text-xl sm:text-2xl md:text-3xl font-semibold"
    data-f_type="h2_">🤝 Contributing</h2>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_">When creating new fragment types:
1. Add to <code>FType</code> enum
2. Implement in <code>FragmentBuilder</code>
3. Add validation rules
4. Create template rendering
5. Document with examples</p>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="h2_">
                <h2 id="support"
    class="fragment text-xl sm:text-2xl md:text-3xl font-semibold"
    data-f_type="h2_">📞 Support</h2>
              </div>
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_">For questions or issues:
- Check existing documentation
- Review example PMs in <code>/pms/examples/</code>
- Look at test files for edge cases
- Consult the fragment builder source</p>
              </div>
          
        
            
            
              
                
                
              
              <div class="fragment-wrapper " data-f_type="hr_">
                <hr class="fragment divider-tight" data-f_type="hr_" />
              </div>
              
            
          
        
            
            
              
              <div class="fragment-wrapper " data-f_type="p_">
                <p class="fragment" data-f_type="p_"><strong>Happy teaching with PM fragments! 🎓</strong></p>
              </div>
          
        
        
        
    
  </div>
  

  <!-- Product Settings Debug (collapsible) -->
  
    <div class="collapse collapse-arrow bg-base-100 mt-4">
      <input type="checkbox" />
      <div class="collapse-title text-sm font-medium">
        Product Settings: <span class="badge badge-primary badge-sm">documentation</span>
        
          <span class="badge badge-error badge-sm ml-2">Not Found</span>
        

      </div>
      <div class="collapse-content">
        
          <div class="alert alert-warning">
            <svg xmlns="http://www.w3.org/2000/svg"
                 class="stroke-current shrink-0 h-6 w-6"
                 fill="none"
                 viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            <div>
              <h3 class="font-bold">No Product Settings Found</h3>
              <div class="text-sm">
                Product "documentation" was not found in the loaded products.
                Check if the product configuration exists in the products/ directory and matches the current domain.
              </div>
            </div>
          </div>
        
      </div>
    </div>
  
  <!-- PM runtime boot -->
  <script type="module">
      import PMRuntime from '@js/pm/main.js';
      const runtime = new PMRuntime({
          mode: 'all'
      });
      if (document.readyState === 'complete' || document.readyState === 'interactive') {
          runtime.init();
      } else {
          window.addEventListener('DOMContentLoaded', () => runtime.init(), {
              once: true
          });
      }
      window.pmRuntime = runtime;
</script>
</div>
</div>
<!-- djlint:on -->

    </main>

    
    

    <!-- Navbar active state management -->
    <script src="../../../static/js/navbar-active-state.js"></script>

  </body>
</html>


<!-- Subscription Call-to-Action
      <section class="my-12 p-6 bg-base-200 rounded-lg text-center">
        <h2 class="text-2xl font-semibold mb-4">
Subscribe to My Newsletter
        </h2>
        <p class="mb-6">
Get the latest posts delivered straight to your inbox.
        </p>
        <form action="/subscribe" method="POST" class="flex justify-center">
          <input type="email" placeholder="Enter your email" class="input input-bordered w-full max-w-xs mr-2" required />
          <button type="submit" class="btn btn-primary">
Subscribe
          </button>
        </form>
      </section>
       -->