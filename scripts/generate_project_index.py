#!/usr/bin/env python3
"""
Script de génération d'index des projets - Brainstorm AI
Génère automatiquement un dashboard exécutif des projets développés
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class ProjectIndexGenerator:
    """Générateur d'index professionnel des projets."""
    
    def __init__(self, exports_dir: str = "data/exports"):
        self.exports_dir = Path(exports_dir)
        self.projects: List[Dict[str, Any]] = []
    
    def scan_projects(self) -> None:
        """Scanne le dossier exports pour identifier les projets."""
        if not self.exports_dir.exists():
            print(f"❌ Dossier d'exports non trouvé : {self.exports_dir}")
            return
        
        project_files = list(self.exports_dir.glob("PROJET_*.md"))
        
        for project_file in sorted(project_files):
            project_info = self._extract_project_info(project_file)
            if project_info:
                self.projects.append(project_info)
    
    def _extract_project_info(self, project_file: Path) -> Dict[str, Any]:
        """Extrait les informations d'un projet depuis son fichier."""
        try:
            with open(project_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extraire le numéro de projet (format: "🚀 PROJET #01" ou "PROJET #1")
            project_match = re.search(r'PROJET #(\d+)', content)
            project_number = int(project_match.group(1)) if project_match else 0
            
            # Extraire le concept principal
            concept_match = re.search(r'## 💡 \*\*CONCEPT PRINCIPAL\*\*\n> (.+)', content)
            concept = concept_match.group(1) if concept_match else "Concept non identifié"
            
            # Extraire la date de création
            date_match = re.search(r'Date de création\*\* \| (.+) \|', content)
            creation_date = date_match.group(1) if date_match else "Date inconnue"
            
            return {
                'number': project_number,
                'filename': project_file.name,
                'concept': concept,
                'creation_date': creation_date,
                'file_size': project_file.stat().st_size,
                'last_modified': datetime.fromtimestamp(project_file.stat().st_mtime)
            }
            
        except Exception as e:
            print(f"⚠️ Erreur lors de l'extraction des infos du projet {project_file}: {e}")
            return None
    
    def generate_dashboard(self) -> str:
        """Génère le dashboard exécutif HTML."""
        total_projects = len(self.projects)
        
        dashboard_content = f"""# 🏆 DASHBOARD EXÉCUTIF - PORTEFEUILLE DE PROJETS

## 📊 **VUE D'ENSEMBLE**

| **Métrique** | **Valeur** |
|--------------|------------|
| **🎯 Projets développés** | **{total_projects}** |
| **📅 Dernière mise à jour** | {datetime.now().strftime('%d/%m/%Y à %H:%M')} |
| **✅ Statut global** | Tous projets finalisés |
| **🚀 Prêts pour mise en œuvre** | **{total_projects}/{total_projects}** |

---

## 🎯 **CATALOGUE DES PROJETS**

### 📋 **Tableau de Bord Interactif**

| **#** | **Concept Principal** | **Statut** | **Priorité** | **Fichier** |
|-------|----------------------|-------------|-------------|-------------|
"""
        
        # Ajouter chaque projet au tableau
        for project in sorted(self.projects, key=lambda x: x['number']):
            concept_short = project['concept'][:50] + "..." if len(project['concept']) > 50 else project['concept']
            dashboard_content += f"| **{project['number']:02d}** | {concept_short} | ✅ Finalisé | ⭐ Haute | [`{project['filename']}`]({project['filename']}) |\n"
        
        dashboard_content += f"""

---

## 🚀 **PROJETS DÉTAILLÉS**

"""
        
        # Ajouter le détail de chaque projet
        for project in sorted(self.projects, key=lambda x: x['number']):
            dashboard_content += f"""### 🎯 **PROJET #{project['number']:02d}**

**💡 Concept :** {project['concept']}

**📅 Créé le :** {project['creation_date']}  
**📄 Fichier :** [`{project['filename']}`]({project['filename']})  
**📊 Taille :** {project['file_size']:,} octets  
**🔄 Modifié :** {project['last_modified'].strftime('%d/%m/%Y à %H:%M')}

**🎯 Actions recommandées :**
- 📋 Réviser le plan d'affaires détaillé
- 💰 Évaluer les besoins en financement
- 👥 Identifier les ressources nécessaires
- 🚀 Planifier la mise en œuvre

---

"""
        
        dashboard_content += f"""## 🎯 **PROCHAINES ÉTAPES STRATÉGIQUES**

### 📈 **Recommandations Exécutives**

1. **🏆 Priorisation** : Classer les {total_projects} projets selon :
   - Impact business estimé
   - Faisabilité technique
   - Ressources disponibles
   - Timeline de mise en œuvre

2. **💰 Évaluation Financière** :
   - Analyser le ROI potentiel de chaque projet
   - Estimer les budgets nécessaires
   - Identifier les sources de financement

3. **🚀 Planification de Déploiement** :
   - Créer un calendrier de lancement
   - Allouer les ressources humaines
   - Définir les jalons et livrables

4. **📊 Suivi et Mesure** :
   - Mettre en place les KPI de suivi
   - Programmer les points de contrôle
   - Préparer le reporting exécutif

---

## 📋 **STATUT GLOBAL DU PORTEFEUILLE**

✅ **{total_projects} projets** développés et finalisés  
✅ **Plans d'affaires** complets et détaillés  
✅ **Analyses critiques** approfondies réalisées  
✅ **Optimisations** intégrées avec succès  
✅ **Prêts pour présentation** aux parties prenantes  

---

*📝 Index généré automatiquement par Brainstorm AI*  
*🤖 Système de brainstorming intelligent multi-agents*  
*📅 Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y à %H:%M')}*
"""
        
        return dashboard_content
    
    def save_dashboard(self, filename: str = "INDEX_PROJETS.md") -> None:
        """Sauvegarde le dashboard dans un fichier."""
        dashboard_content = self.generate_dashboard()
        
        output_file = self.exports_dir / filename
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(dashboard_content)
            
            print(f"✅ Dashboard généré avec succès : {output_file}")
            print(f"📊 {len(self.projects)} projets indexés")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde : {e}")


def main():
    """Fonction principale du script."""
    print("🚀 Génération de l'index des projets - Brainstorm AI")
    print("=" * 50)
    
    generator = ProjectIndexGenerator()
    
    print("🔍 Scan des projets...")
    generator.scan_projects()
    
    if not generator.projects:
        print("❌ Aucun projet trouvé dans le dossier exports")
        return
    
    print(f"📋 {len(generator.projects)} projets trouvés")
    
    print("📝 Génération du dashboard...")
    generator.save_dashboard()
    
    print("✅ Index des projets généré avec succès !")


if __name__ == "__main__":
    main() 