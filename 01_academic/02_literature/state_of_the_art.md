# State of the Art

This chapter contextualises the problem of fetal umbilical vein segmentation within the fields of obstetric imaging and the scientific literature that supports the experimental work developed in this repository. Its purpose is to justify the methodological choices adopted throughout the project—including preprocessing, deep learning-based segmentation, and morphological post-processing—based on clinical knowledge and published evidence, without anticipating the quantitative results obtained.

---

## Clinical and Imaging Context

The umbilical vein plays a fundamental role in fetal circulation, being responsible for transporting oxygenated blood and nutrients from the placenta to the fetus. Any alteration in its structure or function may compromise fetal development and be associated with obstetric complications, intrauterine growth restriction, and increased perinatal morbidity.

Ultrasound imaging is currently the primary technique used for prenatal assessment of the fetal vascular system, enabling non-invasive visualisation of the umbilical cord and its vessels. According to Campos (2017), ultrasound examination of the umbilical cord is essential for the early detection of vascular abnormalities and the monitoring of fetal well-being. The timely identification of such alterations may contribute to more effective clinical intervention and improved pregnancy outcomes.

---

## Anatomical and Ultrasound Literature

The fetal umbilical and portal venous systems have been extensively studied in the literature. Mavrides et al. (2001) provided a detailed description of the anatomy of the umbilical, portal, and hepatic venous systems in fetuses between 14 and 19 weeks of gestation, establishing important anatomical references for the interpretation of ultrasound examinations. Subsequently, Kivilevitch et al. (2009) demonstrated that the use of two-dimensional and three-dimensional ultrasound enables a more detailed evaluation of these vascular structures, facilitating their visualisation and characterisation.

These studies reinforce the clinical importance of accurately delineating the umbilical vein in ultrasound images and justify the use of annotated datasets and automated image analysis methods.

---

## Segmentation Challenges and Computational Motivation

Despite technological advances in fetal imaging, the identification and delineation of the umbilical vein in ultrasound images remain challenging tasks due to the presence of noise, imaging artefacts, and substantial anatomical variability. In this context, the development of automated segmentation methods becomes particularly relevant, offering the potential to improve analysis consistency, reduce operator dependency, and support future computer-aided diagnostic applications.

Consequently, fetal umbilical vein segmentation represents a clinically and scientifically significant problem, contributing both to a more accurate assessment of fetal circulation and to the development of computational tools for prenatal medicine.

---

## Summary and Relation to the Experimental Study

The reviewed literature converges around three key themes that directly support the present project: (1) the clinical importance of the fetal umbilical–portal circulation; (2) the central role of ultrasound imaging in its evaluation; and (3) the need for robust segmentation methods capable of handling image noise and morphological variability.

The experimental study presented in this repository investigates, under controlled conditions, the impact of different preprocessing strategies and morphological operators on the segmentation quality achieved by a deep learning model. This evaluation is conducted using the dataset and experimental protocol described throughout the project documentation (`02_dataset/`, `03_pipeline/`, `04_pipeline_results/`, and `05_report/`).

---

## References

* Campos, C. P. C. (2017). *Patologia do Cordão Umbilical*. Instituto de Ciências Biomédicas Abel Salazar, University of Porto.
* Kivilevitch, Z., Gindes, L., Deutsch, H., & Achiron, R. (2009). *In-utero evaluation of the fetal umbilical–portal venous system: two- and three-dimensional ultrasonic study*. Ultrasound in Obstetrics & Gynecology.
* Mavrides, E., Moscoso, G., Carvalho, J. S., Campbell, S., & Thilaganathan, B. (2001). *The anatomy of the umbilical, portal and hepatic venous systems in the human fetus at 14–19 weeks of gestation*. Ultrasound in Obstetrics & Gynecology.
