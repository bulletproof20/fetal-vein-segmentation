# Estado da Arte

Este capítulo enquadra o problema da segmentação da veia umbilical fetal no contexto da imagiologia obstétrica e da literatura científica que sustenta o trabalho experimental desenvolvido no repositório. O objetivo é situar as escolhas metodológicas — pré-processamento, segmentação por aprendizagem profunda e pós-processamento morfológico — face ao conhecimento clínico e à evidência publicada, sem antecipar os resultados quantitativos obtidos.

---

## Contexto clínico e imagiológico

A veia umbilical desempenha um papel fundamental na circulação fetal, sendo responsável pelo transporte de sangue oxigenado e nutrientes da placenta para o feto. Qualquer alteração na sua estrutura ou funcionamento pode comprometer o desenvolvimento fetal e estar associada a complicações obstétricas, restrição do crescimento intrauterino e aumento da morbilidade perinatal.

A ultrassonografia constitui atualmente a principal técnica de avaliação pré-natal do sistema vascular fetal, permitindo a observação não invasiva do cordão umbilical e dos seus vasos. De acordo com Campos (2017), o estudo ecográfico do cordão umbilical é essencial para a deteção precoce de anomalias vasculares e para a monitorização do bem-estar fetal. A identificação atempada destas alterações pode contribuir para uma intervenção clínica mais eficaz e para a redução de resultados adversos na gravidez.

---

## Literatura anatómica e ecográfica

O sistema venoso umbilical e portal fetal tem sido amplamente estudado na literatura. Mavrides et al. (2001) descreveram detalhadamente a anatomia dos sistemas venoso umbilical, portal e hepático em fetos entre as 14 e as 19 semanas de gestação, estabelecendo referências anatómicas importantes para a interpretação de exames ecográficos. Posteriormente, Kivilevitch et al. (2009) demonstraram que a utilização de ecografia bidimensional e tridimensional permite uma avaliação mais detalhada destas estruturas vasculares, facilitando a sua visualização e caracterização.

Estes trabalhos fundamentam a relevância clínica de delimitar com precisão a veia umbilical em imagens ecográficas e justificam o recurso a bases de dados anotadas e a métodos automáticos de análise.

---

## Desafios da segmentação e motivação computacional

Apesar dos avanços tecnológicos na imagiologia fetal, a identificação e delimitação da veia umbilical em imagens ecográficas continua a ser uma tarefa desafiante devido à presença de ruído, artefactos e elevada variabilidade anatómica. Neste contexto, o desenvolvimento de métodos automáticos de segmentação assume particular relevância, permitindo melhorar a consistência da análise, reduzir a dependência do operador e apoiar futuras aplicações de diagnóstico assistido por computador.

Assim, a segmentação da veia umbilical constitui um problema de interesse clínico e científico, contribuindo para uma avaliação mais rigorosa da circulação fetal e para o desenvolvimento de ferramentas computacionais de apoio à medicina pré-natal.

---

## Síntese e ligação ao estudo experimental

A revisão da literatura converge para três eixos alinhados com o presente projeto: (1) importância clínica da circulação umbilical-portal fetal; (2) papel da ecografia na sua caracterização; (3) necessidade de métodos robustos de segmentação perante ruído e variabilidade morfológica. O estudo experimental que se segue no repositório avalia, de forma controlada, o impacto de estratégias de pré-processamento e de operadores morfológicos sobre a qualidade da segmentação obtida por um modelo de aprendizagem profunda, utilizando o conjunto de dados e o protocolo descritos na documentação do projeto (`02_dataset/`, `03_pipeline/`, `04_pipeline_results/`, `05_report/`).

---

## Referências

* Campos, C. P. C. (2017). *Patologia do Cordão Umbilical*. Instituto de Ciências Biomédicas Abel Salazar, Universidade do Porto.
* Kivilevitch, Z., Gindes, L., Deutsch, H., & Achiron, R. (2009). *In-utero evaluation of the fetal umbilical-portal venous system: two- and three-dimensional ultrasonic study*. Ultrasound in Obstetrics & Gynecology.
* Mavrides, E., Moscoso, G., Carvalho, J. S., Campbell, S., & Thilaganathan, B. (2001). *The anatomy of the umbilical, portal and hepatic venous systems in the human fetus at 14–19 weeks of gestation*. Ultrasound in Obstetrics & Gynecology.
