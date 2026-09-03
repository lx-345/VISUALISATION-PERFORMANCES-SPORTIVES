<div align="center">
  
  <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/High%20Voltage.png" alt="Éclair" width="120" />
  
  <h1>PROJET MEDAS <br> <i>Data Engineering & Cloud-Native</i></h1>

  <p><b>De l'analyse exploratoire locale au déploiement d'une architecture CI/CD robuste.</b></p>

  <!-- Badges technologiques -->
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
    <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubernetes" />
    <img src="https://img.shields.io/badge/MinIO-C7202C?style=for-the-badge&logo=minio&logoColor=white" alt="MinIO" />
  </p>
</div>

<hr>

##  Contexte & Synthèse Rapide

Passionné par la course à pied depuis de nombreuses années (🔗 [Voir mes résultats FFA](https://www.athle.fr/athletes/4014686/resultats)), j'ai souhaité améliorer un projet débuté dans le cadre de mon Master.  Le projet MEDAS est né d'un constat simple : les données GPS (montres, capteurs) sont massives, mais les outils d'analyse de la charge d'entraînement (comme le ratio ACWR) manquent de modularité pour les athlètes amateurs. Tout en sachant l'envergure et la qualité des logiciel d'analyses contemporain comme coros, j'ai  souhaité augemnter l'interactivté de ma solution et offrir un data product transposable à d'autres enjeux métiers. 

Ce projet s'est déroulé en deux phases distinctes :

<table>
  <tr>
    <td width="50%" align="center">
      <h3>🛠️ PHASE 1 : Le Moteur Technique (Local)</h3>
      <p>Modélisation mathématique, nettoyage des données Strava, et génération automatisée de rapports Excel.</p>
      <br>
      <a href="https://github.com/lx-345/PERFORMANCES_SPORTIVES#contexte--la-technicisation-de-la-course-%C3%A0-pied">
        <img src="https://img.shields.io/badge/_VOIR_LE_CODE_V1-3776AB?style=for-the-badge&logo=github&logoColor=white" alt="V1 GitHub" />
      </a>
    </td>
    <td width="50%" align="center">
      <h3>  PHASE 2 : L'Application Web (Cloud)</h3>
      <p>Migration vers une architecture micro-services, conteneurisation Docker et déploiement Kubernetes.</p>
      <br>
      <a href="https://user-paleo-sports.user.lab.sspcloud.fr/">
        <img src="https://img.shields.io/badge/🔴_LANCER_L'APP_V2-FF4B4B?style=for-the-badge&logo=codeigniter&logoColor=white" alt="App en Ligne" />
      </a>
    </td>
  </tr>
</table>

<br>

##  Les 6 Piliers de l'Architecture (Actions Menées)

>  *Cliquez sur les différentes sections ci-dessous pour explorer les choix techniques et les actions menées sur le projet.*

<details>
<summary><b> 1. Architecture du Code (SRP & Src-layout)</b></summary>
<br>
<b>L'objectif :</b> Rendre le code maintenable, lisible et testable.<br>
<b>L'action :</b> J'ai abandonné l'approche "script monolithique" pour adopter un <code>src layout</code> strict généré via <i>uv</i>. Les responsabilités ont été séparées (Principe SRP) : le sous-package <code>analyse_sportive</code> gère la logique d'ingestion S3 et les calculs métier, tandis que le sous-package <code>streamlit_app</code> gère exclusivement le rendu UI et les graphiques <i>Plotly</i>.
<br><br>
</details>

<details>
<summary><b> 2. Ingénierie des Données (Séparation Stockage/Calcul)</b></summary>
<br>
<b>L'objectif :</b> Garantir la reproductibilité et l'accès asynchrone aux données.<br>
<b>L'action :</b> J'ai migré les fichiers CSV locaux vers un <b>Data Lake S3 (MinIO)</b>. Le code lit désormais les données directement en mémoire (via <code>s3fs</code> et <i>Pandas</i>), sans jamais les écrire sur le disque du conteneur. J'ai également séparé la donnée immuable (<i>raw</i>) de la donnée agrégée (<i>processed</i>).
<br><br>
</details>

<details>
<summary><b> 3. Sécurité Minimale & Variables d'Environnement</b></summary>
<br>
<b>L'objectif :</b> Protéger les accès Cloud et sécuriser l'exécution.<br>
<b>L'action :</b> Les identifiants S3 (<i>STS Tokens</i>) ne sont plus codés en dur, mais injectés dynamiquement via des <b>Secrets Kubernetes</b>. Côté Docker, j'ai appliqué le principe du <i>moindre privilège</i> en créant un utilisateur dédié (<code>appuser</code>) dans le <code>Dockerfile</code> pour empêcher l'exécution de l'application avec les droits administrateur (root).
<br><br>
</details>

<details>
<summary><b> 4. Qualité Logicielle & Linting Automatisé</b></summary>
<br>
<b>L'objectif :</b> Maintenir un standard de code irréprochable en équipe.<br>
<b>L'action :</b> J'ai intégré le linter ultra-rapide <b>Ruff</b>. Le respect de la norme PEP-8 est vérifié avant chaque soumission sur le dépôt (blocage des lignes trop longues, nettoyage des imports). Un fichier <code>uv.lock</code> assure le verrouillage déterministe des dépendances.
<br><br>
</details>

<details>
<summary><b> 5. Conteneurisation (Docker)</b></summary>
<br>
<b>L'objectif :</b> Garantir que l'application tourne de manière identique sur n'importe quel environnement.<br>
<b>L'action :</b> L'application, ses dépendances et le framework Streamlit ont été encapsulés dans une image Docker légère, écoutant sur le port 8501, prête à être déployée sur n'importe quel serveur sans conflit d'environnement.
<br><br>
</details>

<details>
<summary><b> 6. Déploiement Continu & IaC (Kubernetes)</b></summary>
<br>
<b>L'objectif :</b> Automatiser la mise en production et assurer la haute disponibilité.<br>
<b>L'action :</b> J'ai rédigé des manifestes YAML (<i>Infrastructure as Code</i>) pour orchestrer l'application sur un cluster Kubernetes. Le flux repose sur un tryptique : <b>Deployment</b> (gestion du Pod), <b>Secret</b> (injection des credentials), et <b>Ingress</b> (routage du trafic web HTTPS).
<br><br>
</details>

<hr>

##   Vue d'ensemble de l'Architecture (Flux de données)

```mermaid
graph TD
    subgraph 1. Data Lake Cloud
        A[(MinIO S3 <br> activites_clean.csv)]
    end
    
    subgraph 2. Cœur d'Application
        B[Backend Métier <br> Calculs ACWR]
        C[Frontend Web <br> Streamlit & Plotly]
        B <--> C
    end
    
    subgraph 3. Infrastructure & Déploiement
        D(GitHub CI <br> Lint + Build Docker)
        E{{Cluster Kubernetes <br> SSPCloud}}
    end
    
    A -->|s3fs / Sécurisé STS| B
    C -->|Conteneurisation| D
    D -->|Déploiement IaC| E
