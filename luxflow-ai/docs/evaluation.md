# Evaluation

The MVP keeps evaluation narrow and useful.

Prompt adherence checks whether the generated clip matches the selected recipe: product, model profile, location, action, lighting, mood, and camera intent.

Product preservation checks whether the handbag remains visually consistent with the source asset. This includes structure, color, handle placement, hardware, logo area, and silhouette.

Other metrics are future work because they require real outputs and broader QA infrastructure. Deferred metrics include temporal consistency, aesthetic scoring, face or identity checks, motion smoothness, artifact detection, and runtime cost.

Current evaluation returns `None` scores with explanatory notes.
