Overview
================

**mbodied agents** offers the following features:

- Configurability : Define your desired Observation and Action spaces and read data into the format that works best for your system.

- Natural Language Control : Use verbal prompts to correct a cognitive agent's actions and calibrate its behavior to a new environment.

- Modularity : Easily swap out different backends, transformers, and hardware interfaces. For even better results, run multiple agents in separate threads.

- Validation : Ensure that your data is in the correct format and that your actions are within the correct bounds before sending them to the robot.

Support Matrix
^^^^^^^^^^^^^^^

If you would like to integrate a new backend, sense, or motion control, it is very easy to do so. Please refer to the `contributing guide <https://github.com/MbodiAI/mbodied-agents/blob/main/CONTRIBUTING.md>`_ for more information.

- OpenAI
- Anthropic
- Mbodi (Coming Soon)
- HuggingFace (Coming Soon)
- Gemini (Coming Soon)

In Beta
^^^^^^^^

For access (or just to say hey 😊), don't hesitate to fill out this `form <https://forms.gle/rv5rovK93dLucma37>`_ or reach out to us at info@mbodi.ai.

- **Conductor**: A service for processing and managing datasets, and automatically training your models on your own data.

- **Conductor Dashboard**: See how GPT-4o, Claude Opus, or your custom models are performing on your datasets and open benchmarks.

- **Data Augmentation**: Build invariance to different environments by augmenting your dataset with Mbodi's diffusion-based data augmentation to achieve better generalization.

- **Mbodied SVLM**: A new Spatial Vision Language Model trained specifically for spatial reasoning and robotics control.

Idea
^^^^^^

The core idea behind **mbodied agents** is end-to-end continual learning. We believe that the best way to train a robot is to have it learn from its own experiences.