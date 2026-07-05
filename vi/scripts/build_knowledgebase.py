#!/usr/bin/env python3
"""
Tennis Knowledgebase Hub - Concept Nodes Generator

Builds 80-100 concept nodes from tennisplayer.net source topics.
Each node = a single tennis concept with original description (200-400 words).
No verbatim text from source - all content is original synthesis.

Structure:
  docs/tennisplayer/
    index.md                          (hub - all 80+ nodes organized)
    <sub-library>/
      index.md                        (per-section node list)
      <concept-slug>.md               (one concept per file)
"""
from pathlib import Path
import unicodedata
import re

DST = Path(r"C:\Users\Henry\Documents\tennis-wiki\docs\tennisplayer")

# ============================================================
# CONCEPT TAXONOMY
# ============================================================
# Each node: (slug, title, category, sub_library, description_summary, related_slugs)
# All descriptions are ORIGINAL - synthesized tennis knowledge, no verbatim from source.

CONCEPTS = [
    # ============== ULTIMATE FUNDAMENTALS (8 nodes) ==============
    {
        "slug": "modern-forehand-fundamentals",
        "title": "The Modern Forehand — Foundation",
        "sub_library": "ultimate-fundamentals",
        "summary": "The modern forehand is the cornerstone weapon of contemporary tennis. Unlike the flat, arm-driven forehand of earlier eras, today's version is a kinetic chain event: ground reaction forces travel from the legs through the hips, rotate the torso, and whip the relaxed arm into the ball. The signature shape is a low-to-high swing path with heavy topspin, allowing aggressive baseline play with margin over the net.",
        "related": ["kinetic-chain", "ground-reaction-forces", "lag-mechanics", "open-stance-forehand", "modern-backhand"],
    },
    {
        "slug": "modern-backhand",
        "title": "The Modern Backhand — Two-Handed Foundation",
        "sub_library": "ultimate-fundamentals",
        "summary": "The two-handed backhand is the modern standard for players below professional level. It stabilizes the stroke against incoming pace, allows for powerful rotation through the kinetic chain, and provides a wider margin for error than the one-handed version. The dominant hand drives the swing while the non-dominant hand provides control and power.",
        "related": ["modern-forehand-fundamentals", "one-handed-backhand-slice", "kinetic-chain", "backhand-biomechanics"],
    },
    {
        "slug": "one-handed-backhand-slice",
        "title": "The One-Handed Backhand Slice",
        "sub_library": "ultimate-fundamentals",
        "summary": "The slice backhand is a strategic tool that uses underspin to keep the ball low, neutralize pace, and buy recovery time. Unlike topspin groundstrokes that require full body rotation, the slice can be hit with a more compact motion, making it useful in defensive situations and as a setup shot. Champions like Federer demonstrated that the slice remains elite when used with precision and disguise.",
        "related": ["one-handed-topspin-backhand", "modern-backhand", "defensive-strategies", "net-rush"],
    },
    {
        "slug": "one-handed-topspin-backhand",
        "title": "The One-Handed Topspin Backhand",
        "sub_library": "ultimate-fundamentals",
        "summary": "A high-risk, high-reward stroke requiring exceptional technique, timing, and strength. The one-handed topspin backhand opens up the court to attacking down-the-line shots and angles, but demands precise footwork and pre-loading the kinetic chain. Modern usage is rare at elite level, but the stroke remains a beautiful and effective weapon in the right hands.",
        "related": ["one-handed-backhand-slice", "modern-backhand", "backhand-biomechanics", "kinetic-chain"],
    },
    {
        "slug": "serve-fundamentals",
        "title": "The Serve — Foundational Mechanics",
        "sub_library": "ultimate-fundamentals",
        "summary": "The serve is the only stroke in tennis where the player has complete control from start to finish. The kinetic chain sequence is: legs load, hips rotate, shoulders tilt, racquet drops behind the back, forearm pronates through contact. The trophy pose is the moment of maximum loaded energy, and the pronation at contact is what generates pace and spin without straining the shoulder.",
        "related": ["kinetic-chain", "rhythm-relaxation", "leg-drive", "spin-vs-flat-serve"],
    },
    {
        "slug": "volley-fundamentals",
        "title": "The Volley — Compact Net Play",
        "sub_library": "ultimate-fundamentals",
        "summary": "Modern volleys emphasize compactness, structure, and using the opponent's pace. The continental grip is essential. Rather than swinging at the ball, the volley redirects it through a stable wrist and short punch motion. The split step as the opponent strikes the ball pre-loads the legs for instant lateral movement.",
        "related": ["split-step", "net-rush", "approach-shot", "kinetic-chain"],
    },
    {
        "slug": "forehand-volley",
        "title": "The Forehand Volley",
        "sub_library": "ultimate-fundamentals",
        "summary": "The forehand volley is the offensive weapon at net, typically used for put-aways and angle creation. It uses the continental grip for versatility between flat punches and slight underspin. The motion is a short, firm punch forward rather than a full swing, with the non-dominant hand often used to track the ball and maintain balance.",
        "related": ["volley-fundamentals", "backhand-volley", "net-rush", "continental-grip"],
    },
    {
        "slug": "backhand-volley",
        "title": "The Backhand Volley",
        "sub_library": "ultimate-fundamentals",
        "summary": "The backhand volley is a defensive and reactive shot, often used to neutralize aggressive approaches. The compact continental grip allows quick transition from forehand to backhand volleys. The key is a short punch with the dominant hand guiding the racquet face, with body shoulder turn providing power rather than arm swing.",
        "related": ["volley-fundamentals", "forehand-volley", "net-rush", "split-step"],
    },

    # ============== ULTIMATE DRILL GAMES (8 nodes) ==============
    {
        "slug": "competitive-drills",
        "title": "Competitive Drill Games for Training",
        "sub_library": "ultimate-drill-games",
        "summary": "Drill games combine technical practice with competitive pressure, mimicking match conditions while reinforcing stroke patterns. The best drill games have clear scoring, point consequences, and progressive difficulty. Examples: 'King of the Court' rotations, target zones with bonus points, and timed challenges that simulate tiebreak scenarios.",
        "related": ["match-simulation-drills", "pressure-training", "deliberate-practice", "split-step"],
    },
    {
        "slug": "match-simulation-drills",
        "title": "Match Simulation Drills",
        "sub_library": "ultimate-drill-games",
        "summary": "Match simulation drills replicate the chaos of real tennis: random feeds, varied spin, pressure scenarios, and decision-making under fatigue. Unlike mechanical ball-machine drills, these require the player to read, decide, and execute as in competition. Coaches use constraints (e.g., must hit 3 crosscourt before changing direction) to build intelligent shot selection.",
        "related": ["competitive-drills", "deliberate-practice", "decision-making", "percentage-tennis"],
    },
    {
        "slug": "point-play-progression",
        "title": "Point Play Progression",
        "sub_library": "ultimate-drill-games",
        "summary": "A teaching progression that starts with cooperative rallies and gradually adds competitive elements. Stage 1: cooperative crosscourt rallies. Stage 2: cooperative with direction change. Stage 3: live points with constraints. Stage 4: live points with scoring. This builds tactical awareness alongside technical improvement.",
        "related": ["match-simulation-drills", "competitive-drills", "deliberate-practice", "percentage-tennis"],
    },
    {
        "slug": "pressure-training",
        "title": "Pressure Training Games",
        "sub_library": "ultimate-drill-games",
        "summary": "Pressure training games create high-stakes scenarios in practice: must-win points, consequences for errors, audience involvement, or bet-style scoring. The goal is to normalize pressure so the player performs consistently in competition. Research shows players who train under simulated pressure make fewer errors in actual matches.",
        "related": ["competitive-drills", "mental-toughness", "between-point-routines", "percentage-tennis"],
    },
    {
        "slug": "live-ball-drills",
        "title": "Live Ball Drills",
        "sub_library": "ultimate-drill-games",
        "summary": "Live ball drills use a coach or partner feeding balls in patterns that simulate match play while allowing repetition. Examples: alternating forehand/backhand patterns, deep-to-short progressions, and approach-shot + volley sequences. These drills bridge the gap between isolated stroke practice and full match play.",
        "related": ["match-simulation-drills", "approach-shot", "split-step", "kinetic-chain"],
    },
    {
        "slug": "group-lesson-games",
        "title": "Group Lesson Games",
        "sub_library": "ultimate-drill-games",
        "summary": "Group lesson games maximize engagement and touches per player in a multi-player setting. Common formats: round-robin rotations, elimination tournaments, target challenges, and team-based competitions. Effective group games keep all players active simultaneously, building fitness, social engagement, and stroke consistency.",
        "related": ["competitive-drills", "pressure-training", "match-simulation-drills", "deliberate-practice"],
    },
    {
        "slug": "junior-tennis-games",
        "title": "Junior Tennis Games",
        "sub_library": "ultimate-drill-games",
        "summary": "Junior tennis games use age-appropriate themes, scoring, and equipment to engage young players. The best junior games disguise repetition as play: relay races with racquets, animal-themed movement drills, and character-based stroke stories. The goal is technical repetition without boring repetition.",
        "related": ["group-lesson-games", "pressure-training", "deliberate-practice", "competitive-drills"],
    },
    {
        "slug": "warm-up-routines",
        "title": "Effective Warm-Up Routines",
        "sub_library": "ultimate-drill-games",
        "summary": "A proper warm-up progresses from general to specific: light cardio for blood flow, dynamic stretching for range of motion, footwork patterns for activation, mini-tennis for touch, baseline rallies for rhythm, and then specific stroke patterns. Skipping steps or jumping into full-intensity hitting is a common cause of early-match injuries.",
        "related": ["deliberate-practice", "match-simulation-drills", "split-step", "rhythm-relaxation"],
    },

    # ============== TEACHING SYSTEMS (6 nodes) ==============
    {
        "slug": "teaching-progression",
        "title": "Tennis Teaching Progression",
        "sub_library": "teaching-systems",
        "summary": "A structured progression moves students from beginner to advanced through carefully sequenced stages. The traditional progression: grips and stance, basic strokes from short court, rallying skills, point play, patterns, and finally tactical match play. Each stage builds on the previous and introduces new concepts at the right developmental moment.",
        "related": ["deliberate-practice", "point-play-progression", "match-simulation-drills", "kinetic-chain"],
    },
    {
        "slug": "private-vs-group-lessons",
        "title": "Private vs Group Lessons",
        "sub_library": "teaching-systems",
        "summary": "Private lessons offer personalized attention and faster progress on specific issues, while group lessons provide more touches per hour, social pressure, and varied playing styles. The optimal mix depends on the student's level: beginners benefit from group foundations, intermediate players need private technical work, and advanced players need both tactical private sessions and competitive group play.",
        "related": ["teaching-progression", "group-lesson-games", "deliberate-practice", "competitive-drills"],
    },
    {
        "slug": "video-analysis",
        "title": "Video Analysis for Tennis",
        "sub_library": "teaching-systems",
        "summary": "Video analysis reveals what the player feels vs what is actually happening. The most useful angles are side view (for stroke mechanics, contact point, posture) and rear view (for stance, footwork, spacing). Recording practice and matches, then reviewing with a coach or alone, accelerates improvement more than any other single tool.",
        "related": ["deliberate-practice", "self-coaching", "kinetic-chain", "contact-point"],
    },
    {
        "slug": "self-coaching",
        "title": "Self-Coaching Methods",
        "sub_library": "teaching-systems",
        "summary": "Self-coaching combines video review, journaling, and structured self-assessment. The most effective practice: record a session, identify one specific issue, design a drill for it, and track progress over weeks. A simple scoring system (1-10 on contact quality, depth, direction) provides objective feedback without a coach present.",
        "related": ["video-analysis", "deliberate-practice", "between-point-routines", "match-simulation-drills"],
    },
    {
        "slug": "coaching-communication",
        "title": "Effective Coaching Communication",
        "sub_library": "teaching-systems",
        "summary": "Effective coaches use concise, positive cues: 'toss high', 'low to high', 'split then push'. They focus on one adjustment at a time, prioritize feel over technical jargon, and ask the student to describe what they feel. The best coaches are 80% question-asker and 20% instructor.",
        "related": ["teaching-progression", "self-coaching", "video-analysis", "deliberate-practice"],
    },
    {
        "slug": "error-correction",
        "title": "Error Correction in Tennis",
        "sub_library": "teaching-systems",
        "summary": "Effective error correction identifies the root cause, not just the symptom. A forehand going long might be from late contact, poor weight transfer, or a stiff wrist. Coaches use targeted questions, demonstrations, and progressive constraints to isolate the issue. Correcting one element at a time prevents overwhelm.",
        "related": ["self-coaching", "video-analysis", "teaching-progression", "kinetic-chain"],
    },

    # ============== FAMOUS COACHES (6 nodes) ==============
    {
        "slug": "famous-coaches-overview",
        "title": "Tennis Coaching Legends",
        "sub_library": "famous-coaches",
        "summary": "Tennis coaching history is rich with influential figures who shaped modern technique: Dennis Ralston's footwork emphasis, Nick Bollettieri's academy system, Robert Lansdorp's mental toughness focus, and many others. Each major coach developed signature methodologies that influenced how the game is taught today.",
        "related": ["coaching-communication", "teaching-progression", "self-coaching", "mental-toughness"],
    },
    {
        "slug": "european-coaching-philosophy",
        "title": "European Coaching Philosophy",
        "sub_library": "famous-coaches",
        "summary": "European coaching traditions, particularly Spanish and French, emphasize technical precision, patience in building strokes, and tactical intelligence. The Spanish 'metodologia' builds players through repetitive structured drills before introducing match play. French tennis historically produced elegant tacticians like Noah and Santoro.",
        "related": ["famous-coaches-overview", "teaching-progression", "deliberate-practice", "tactical-tennis"],
    },
    {
        "slug": "american-coaching-philosophy",
        "title": "American Coaching Philosophy",
        "sub_library": "famous-coaches",
        "summary": "American tennis coaching historically emphasized aggressive baseline play, big serves, and athleticism. The Bollettieri academy model produced baseline powerhouses. Modern American coaching has integrated more tactical and physical preparation from European and Australian traditions.",
        "related": ["famous-coaches-overview", "european-coaching-philosophy", "athletic-development", "percentage-tennis"],
    },
    {
        "slug": "modern-coaches-impact",
        "title": "Impact of Modern Coaches on Tour",
        "sub_library": "famous-coaches",
        "summary": "Today's top coaches work intimately with elite players, providing tactical advice, mental preparation, and stroke refinement. The relationship between coach and player has become more collaborative. Coaches like Darren Cahill (Agassi, Sinner), Toni Nadal (early Nadal), and Patrick Mouratoglou (later Serena) have shaped champions' careers.",
        "related": ["famous-coaches-overview", "tactical-tennis", "mental-toughness", "between-point-routines"],
    },
    {
        "slug": "coaching-academies",
        "title": "Tennis Academies Worldwide",
        "sub_library": "famous-coaches",
        "summary": "Major academies like Bollettieri, Mouratoglou, Sanchez-Casal, and others have developed systems for producing professional players. These combine intensive training, sports science, mental coaching, and match play. Modern academies often partner with universities to provide balanced development.",
        "related": ["famous-coaches-overview", "european-coaching-philosophy", "athletic-development", "deliberate-practice"],
    },
    {
        "slug": "private-coach-selection",
        "title": "Choosing a Private Coach",
        "sub_library": "famous-coaches",
        "summary": "Selecting a private coach depends on your goals, level, and learning style. Look for: certified credentials (PTR, USPTA, ITF), experience with players at your level, a clear teaching philosophy, and good communication. The best coach for you is one whose methods match how you learn and who challenges you appropriately.",
        "related": ["private-vs-group-lessons", "famous-coaches-overview", "coaching-communication", "self-coaching"],
    },

    # ============== CLASSIC LESSONS (10 nodes) ==============
    {
        "slug": "kinetic-chain",
        "title": "The Kinetic Chain in Tennis",
        "sub_library": "classic-lessons",
        "summary": "The kinetic chain is the sequential transfer of energy from the ground through the body to the racquet. Power is generated from the legs pushing into the ground, transferred through the hips, rotated through the torso, and finally whipped through the arm. Breaking the chain at any point (locked legs, stiff core, early arm swing) reduces power and increases injury risk.",
        "related": ["ground-reaction-forces", "separation-angle", "lag-mechanics", "rhythm-relaxation"],
    },
    {
        "slug": "ground-reaction-forces",
        "title": "Ground Reaction Forces (GRF) in Tennis",
        "sub_library": "classic-lessons",
        "summary": "Ground reaction forces are the upward push from the court in response to a player pushing down. Elite players push hard into the ground to generate explosive upward and rotational force. Studies show professional players can produce forces up to 2-3 times their body weight through proper leg drive.",
        "related": ["kinetic-chain", "leg-drive", "open-stance-forehand", "serve-fundamentals"],
    },
    {
        "slug": "open-stance-forehand",
        "title": "Open Stance Forehand",
        "sub_library": "classic-lessons",
        "summary": "The open stance forehand allows full hip and shoulder rotation, generating power through separation and pelvic rotation rather than linear weight transfer. Modern baseline play relies on the open stance to handle high-bouncing balls and to recover quickly to the center. The outside leg is the key to loading and exploding into the shot.",
        "related": ["kinetic-chain", "separation-angle", "lag-mechanics", "ground-reaction-forces"],
    },
    {
        "slug": "contact-point",
        "title": "Contact Point in Tennis",
        "sub_library": "classic-lessons",
        "summary": "The contact point is where the ball meets the strings, and it determines the consistency, power, and direction of every shot. For groundstrokes, the ideal contact is out in front of the body, at a comfortable height (waist to chest for forehands, knee to waist for low balls). Inconsistent contact is the primary cause of errors.",
        "related": ["spacing", "footwork-patterns", "kinetic-chain", "lag-mechanics"],
    },
    {
        "slug": "spacing",
        "title": "Spacing and Court Positioning",
        "sub_library": "classic-lessons",
        "summary": "Proper spacing means being at the right distance from the ball at contact, neither too close nor too far. Elite players constantly adjust their spacing through split steps, recovery steps, and anticipation. Poor spacing is the root cause of most contact errors and rushed swings.",
        "related": ["contact-point", "split-step", "footwork-patterns", "recovery-footwork"],
    },
    {
        "slug": "rhythm-relaxation",
        "title": "Rhythm and Relaxation",
        "sub_library": "classic-lessons",
        "summary": "Tension is the enemy of fluidity and pace. Elite players use selective relaxation: tense only at the moment of contact, relaxed through preparation and follow-through. The breath pattern matters too: exhale at contact to release tension. Mastering relaxation improves racquet head speed and reduces fatigue.",
        "related": ["kinetic-chain", "lag-mechanics", "between-point-routines", "mental-toughness"],
    },
    {
        "slug": "separation-angle",
        "title": "Hip-Shoulder Separation (X-Factor)",
        "sub_library": "classic-lessons",
        "summary": "The angle between the hips and shoulders during preparation creates elastic energy in the core. When the hips begin to open while the shoulders remain turned, the trunk stretches like a coiled spring. This stored elastic energy releases explosively at contact, adding power without muscular effort.",
        "related": ["kinetic-chain", "open-stance-forehand", "lag-mechanics", "pelvic-snap"],
    },
    {
        "slug": "pelvic-snap",
        "title": "The Pelvic Snap",
        "sub_library": "classic-lessons",
        "summary": "The pelvic snap is the explosive rotation of the pelvis that initiates the kinetic chain in modern groundstrokes. It works in combination with hip-shoulder separation: the pelvis rotates first, loading energy in the core, then releases to whip the upper body through contact. The outside leg braces to create a stable rotation axis.",
        "related": ["separation-angle", "kinetic-chain", "open-stance-forehand", "lag-mechanics"],
    },
    {
        "slug": "lag-mechanics",
        "title": "Racquet Lag in Modern Tennis",
        "sub_library": "classic-lessons",
        "summary": "Racquet lag is the delay of the racquet head behind the hand during the forward swing, created by the relaxed wrist and forearm combined with proper sequencing. This lag acts like a whip, building speed at the moment of contact. Forced wrist bending is the wrong way to create lag—it must come from proper kinetic chain sequencing.",
        "related": ["kinetic-chain", "pat-the-dog", "rhythm-relaxation", "windshield-wiper"],
    },
    {
        "slug": "spin-vs-flat-serve",
        "title": "Spin Serve vs Flat Serve",
        "sub_library": "classic-lessons",
        "summary": "The flat serve maximizes pace with minimal spin, ideal for first serves when the player has time to set up. The kick serve uses heavy topspin for high bounce, making it ideal for second serves and high-margin first serves. The slice serve curves laterally, useful for pulling opponents off the court.",
        "related": ["serve-fundamentals", "second-serve-tactics", "leg-drive", "tactical-tennis"],
    },

    # ============== FOOTWORK (6 nodes) ==============
    {
        "slug": "split-step",
        "title": "The Split Step",
        "sub_library": "footwork",
        "summary": "The split step is a small timed hop that pre-loads the leg muscles and synchronizes the nervous system just before the opponent strikes the ball. Timing is critical: the feet should land on the court as the opponent's racquet makes contact. This pre-load allows instant explosive movement in any direction.",
        "related": ["footwork-patterns", "recovery-footwork", "first-step", "movement-efficiency"],
    },
    {
        "slug": "footwork-patterns",
        "title": "Tennis Footwork Patterns",
        "sub_library": "footwork",
        "summary": "Tennis footwork follows identifiable patterns: the split-step, the first explosive step (often a crossover or shuffle), adjustment steps to fine-tune spacing, the contact step, and the recovery. Elite players move with intention and pattern, not random scrambling.",
        "related": ["split-step", "recovery-footwork", "first-step", "crossover-step"],
    },
    {
        "slug": "recovery-footwork",
        "title": "Recovery Footwork",
        "sub_library": "footwork",
        "summary": "Recovery is the often-neglected third of tennis footwork (the others being approach and contact). After every shot, the player must recover to the optimal court position. Elite players use the split-step before the next ball, not just to start the rally.",
        "related": ["split-step", "court-positioning", "footwork-patterns", "first-step"],
    },
    {
        "slug": "crossover-step",
        "title": "The Crossover Step",
        "sub_library": "footwork",
        "summary": "The crossover step is an explosive lateral movement where the outside foot crosses in front of the inside foot. It allows the player to cover ground quickly to reach wide balls, far more efficient than shuffling. The hip rotation initiates the move, and the plant leg absorbs the deceleration.",
        "related": ["footwork-patterns", "split-step", "shuffle-step", "first-step"],
    },
    {
        "slug": "shuffle-step",
        "title": "The Shuffle Step",
        "sub_library": "footwork",
        "summary": "The shuffle step is a lateral movement pattern useful for short distances and maintaining balance. Unlike the crossover, shuffling keeps the feet parallel and is more efficient for small adjustments. The split-step leads into either a shuffle or a crossover depending on the ball's distance.",
        "related": ["footwork-patterns", "crossover-step", "split-step", "movement-efficiency"],
    },
    {
        "slug": "first-step",
        "title": "The First Step Principle",
        "sub_library": "footwork",
        "summary": "The first explosive step after the split-step is the most important movement in tennis. Players who win the first step win the point more often. The first step should be aggressive and committed, in the direction dictated by the opponent's shot, not hesitant or reactive.",
        "related": ["split-step", "crossover-step", "footwork-patterns", "reaction-time"],
    },

    # ============== STRATEGY AND STATISTICS (8 nodes) ==============
    {
        "slug": "percentage-tennis",
        "title": "Percentage Tennis",
        "sub_library": "strategy-and-statistics",
        "summary": "Percentage tennis is the strategy of playing high-percentage shots: crosscourt over down-the-line, deep over short, high-margin over low-margin. The goal is to make fewer unforced errors than the opponent, not to hit spectacular winners. Statistical analysis shows crosscourt shots win more points per attempt than down-the-line.",
        "related": ["tactical-tennis", "court-positioning", "between-point-routines", "match-simulation-drills"],
    },
    {
        "slug": "tactical-tennis",
        "title": "Tactical Patterns in Tennis",
        "sub_library": "strategy-and-statistics",
        "summary": "Tactical patterns are pre-planned shot sequences that exploit court geometry, opponent weaknesses, and timing. Examples: serve-and-volley, serve-plus-one, baseline attrition, attack-the-backhand. The best players have 2-3 reliable patterns they can execute under pressure.",
        "related": ["percentage-tennis", "court-positioning", "match-simulation-drills", "opponent-analysis"],
    },
    {
        "slug": "court-positioning",
        "title": "Court Positioning Strategy",
        "sub_library": "strategy-and-statistics",
        "summary": "Court positioning is the art of being in the right place at the right time. Baseline players should stand slightly behind the baseline to buy reaction time. Net players should close to the service line or closer. The optimal position changes based on the opponent's position, the shot's pace, and the game situation.",
        "related": ["percentage-tennis", "tactical-tennis", "recovery-footwork", "net-rush"],
    },
    {
        "slug": "opponent-analysis",
        "title": "Opponent Analysis and Scouting",
        "sub_library": "strategy-and-statistics",
        "summary": "Effective opponent analysis identifies weaknesses, patterns, and tendencies. Watch the warm-up: forehand grip, serve toss, movement patterns. Look for: weaker side (often backhand), preferred patterns, vulnerabilities under pressure, and physical limitations. Build your strategy around the opponent's weakness, not your strength.",
        "related": ["tactical-tennis", "percentage-tennis", "match-simulation-drills", "between-point-routines"],
    },
    {
        "slug": "serve-plus-one",
        "title": "Serve +1 Strategy",
        "sub_library": "strategy-and-statistics",
        "summary": "The serve +1 is the second shot after the serve, designed to put the opponent on the defensive. A wide slice serve pulls the opponent off court, opening the court for a forehand to the open space. A body serve jams the opponent, setting up a forehand to either side. The serve +1 wins more points than the serve itself.",
        "related": ["tactical-tennis", "percentage-tennis", "spin-vs-flat-serve", "approach-shot"],
    },
    {
        "slug": "return-positioning",
        "title": "Return of Serve Positioning",
        "sub_library": "strategy-and-statistics",
        "summary": "The return position affects both reaction time and the resulting shot. Standing closer to the baseline gives more time but less reaction window. Standing deeper gives more time to read the serve. Elite returners adjust position based on server tendencies, score, and surface.",
        "related": ["return-strategy", "split-step", "footwork-patterns", "tactical-tennis"],
    },
    {
        "slug": "between-point-routines",
        "title": "Between-Point Routines",
        "sub_library": "strategy-and-statistics",
        "summary": "Consistent between-point routines are critical for mental reset and tactical planning. A typical routine: walk behind the baseline (mental break), check the score, decide on the next point's intent, take a deep breath, then approach the line. The routine should take 15-25 seconds.",
        "related": ["mental-toughness", "percentage-tennis", "tactical-tennis", "pressure-training"],
    },
    {
        "slug": "match-statistics",
        "title": "Match Statistics and Analytics",
        "sub_library": "strategy-and-statistics",
        "summary": "Modern tennis is increasingly data-driven. Key statistics include: first serve percentage, winners vs unforced errors, break point conversion, and shot placement heatmaps. Players can use post-match analytics to identify patterns and adjust strategy. Even amateur players benefit from tracking simple stats like first-serve percentage.",
        "related": ["percentage-tennis", "tactical-tennis", "opponent-analysis", "self-coaching"],
    },

    # ============== MENTAL GAME (8 nodes) ==============
    {
        "slug": "mental-toughness",
        "title": "Mental Toughness in Tennis",
        "sub_library": "mental-game",
        "summary": "Mental toughness is the ability to maintain focus, confidence, and emotional control under pressure. It is not about being emotionless, but about channeling emotions productively. The components: self-belief, emotional regulation, focus control, and motivation. Mental toughness is trainable, not innate.",
        "related": ["between-point-routines", "pressure-training", "confidence", "visualization"],
    },
    {
        "slug": "visualization",
        "title": "Visualization and Mental Imagery",
        "sub_library": "mental-game",
        "summary": "Visualization (or mental imagery) is the practice of vividly imagining successful execution of tennis strokes and match situations. Research shows visualization activates similar neural pathways as physical practice. Effective visualization includes all senses: sight, sound, feel, even smell. Rehearse both successful outcomes and recovery from errors.",
        "related": ["mental-toughness", "deliberate-practice", "confidence", "pre-match-routine"],
    },
    {
        "slug": "confidence",
        "title": "Building Tennis Confidence",
        "sub_library": "mental-game",
        "summary": "Confidence in tennis comes from preparation, not from positive self-talk alone. The formula: build a strong technical base, then accumulate evidence of success in practice. Confidence under pressure comes from having a reliable routine and trusting the trained stroke. False confidence collapses under stress; earned confidence holds.",
        "related": ["mental-toughness", "deliberate-practice", "pre-match-routine", "between-point-routines"],
    },
    {
        "slug": "pre-match-routine",
        "title": "Pre-Match Routine",
        "sub_library": "mental-game",
        "summary": "A consistent pre-match routine primes the body and mind for competition. Components: physical warm-up (10-20 minutes), dynamic stretching, hitting progression (mini-tennis, baseline, patterns), and mental preparation (visualization, tactical review). The routine should be the same for every match to signal the brain it's time to compete.",
        "related": ["warm-up-routines", "visualization", "mental-toughness", "between-point-routines"],
    },
    {
        "slug": "focus-and-concentration",
        "title": "Focus and Concentration",
        "sub_library": "mental-game",
        "summary": "Tennis focus oscillates between broad (whole court awareness) and narrow (specific point focus). The best players maintain 'soft focus': aware of the full court, opponent, and their own body, without fixating on any single element. Practice focusing on process (your own stroke) rather than outcome (winning the point).",
        "related": ["mental-toughness", "between-point-routines", "visualization", "pressure-training"],
    },
    {
        "slug": "emotional-control",
        "title": "Emotional Control Under Pressure",
        "sub_library": "mental-game",
        "summary": "Emotional control is the ability to stay calm and clear-headed in high-pressure situations. Techniques: breath control (4-7-8 breathing), physical reset routines, and cognitive reframing ('this is a fun challenge' rather than 'I must win'). Accept that pressure is part of competition, then channel it.",
        "related": ["mental-toughness", "between-point-routines", "pressure-training", "focus-and-concentration"],
    },
    {
        "slug": "handling-errors",
        "title": "Handling Errors in Matches",
        "sub_library": "mental-game",
        "summary": "How a player handles errors often determines match outcomes. The '15-second rule': after a mistake, take 15 seconds to acknowledge it, let it go, and refocus. Avoid dwelling on errors or making technical adjustments during matches. Save analysis for practice, execute the trained stroke in competition.",
        "related": ["mental-toughness", "between-point-routines", "emotional-control", "deliberate-practice"],
    },
    {
        "slug": "muscle-memory",
        "title": "Muscle Memory and Motor Learning",
        "sub_library": "mental-game",
        "summary": "Muscle memory (more accurately, motor learning) is the process by which repeated practice creates automatic, unconscious motor patterns. The key to building muscle memory: thousands of quality repetitions, ideally in varied conditions. Sleep is essential for motor memory consolidation—practice without adequate sleep is largely wasted.",
        "related": ["deliberate-practice", "visualization", "kinetic-chain", "mental-toughness"],
    },

    # ============== ADVANCED TENNIS (10 nodes) ==============
    {
        "slug": "pat-the-dog",
        "title": "Pat the Dog — Forehand Slot Position",
        "sub_library": "advanced-tennis",
        "summary": "The 'pat the dog' position is the low point in the modern forehand's swing path, where the racquet head drops below the ball with the strings facing down. This position is gravity-assisted, not muscle-forced. From this low position, the racquet accelerates upward and forward, brushing up the back of the ball for topspin.",
        "related": ["lag-mechanics", "kinetic-chain", "windshield-wiper", "modern-forehand-fundamentals"],
    },
    {
        "slug": "windshield-wiper",
        "title": "The Windshield Wiper Forehand",
        "sub_library": "advanced-tennis",
        "summary": "The windshield wiper describes the modern forehand follow-through where the racquet brushes up the back of the ball and finishes across the body, like a windshield wiper. The motion is the natural result of proper sequencing and relaxed forearm pronation, not a forced shape. It generates heavy topspin and clean contact.",
        "related": ["pat-the-dog", "lag-mechanics", "kinetic-chain", "modern-forehand-fundamentals"],
    },
    {
        "slug": "approach-shot",
        "title": "The Approach Shot",
        "sub_library": "advanced-tennis",
        "summary": "The approach shot sets up the net rush. It should be deep, well-placed, and have enough pace or spin to force a weak reply. Common approach patterns: deep crosscourt slice, deep body shot, or short angle. The shot quality is less important than the result: a reply you can volley.",
        "related": ["net-rush", "volley-fundamentals", "tactical-tennis", "percentage-tennis"],
    },
    {
        "slug": "net-rush",
        "title": "Net Rush Tactics",
        "sub_library": "advanced-tennis",
        "summary": "Coming to the net is high-risk, high-reward. Success depends on: quality approach shot, split step as opponent strikes, first volley placement, and recovery for the second volley. Modern players use the net rush selectively, often as a surprise pattern rather than a default strategy.",
        "related": ["approach-shot", "volley-fundamentals", "tactical-tennis", "split-step"],
    },
    {
        "slug": "return-strategy",
        "title": "Return of Serve Strategy",
        "sub_library": "advanced-tennis",
        "summary": "Effective return strategy combines compact mechanics with intelligent placement. The goal: neutralize the server's advantage and seize initiative. Most returners stand deep for reaction time. The compact, blocked return uses the server's pace to redirect the ball deep. Aggressive returners step in on second serves for high-percentage attacks.",
        "related": ["return-positioning", "split-step", "tactical-tennis", "footwork-patterns"],
    },
    {
        "slug": "passing-shots",
        "title": "Passing Shots",
        "sub_library": "advanced-tennis",
        "summary": "Passing shots are weapons used to defeat a net rusher. The down-the-line passing shot is the most direct but requires precise timing. The crosscourt angle is safer but leaves more court for the volleyer. Key elements: disguise, depth, and pace. The lob is a valid passing shot when the opponent is close to the net.",
        "related": ["net-rush", "approach-shot", "tactical-tennis", "lob"],
    },
    {
        "slug": "lob",
        "title": "The Lob",
        "sub_library": "advanced-tennis",
        "summary": "The lob is a strategic shot that goes over the opponent's head. The defensive lob is high and deep, used to buy time against a net rusher. The offensive lob is topspin and precise, used to win the point outright. Both require good touch and reading of court position.",
        "related": ["passing-shots", "net-rush", "tactical-tennis", "percentage-tennis"],
    },
    {
        "slug": "drop-shot",
        "title": "The Drop Shot",
        "sub_library": "advanced-tennis",
        "summary": "The drop shot is a soft shot that just clears the net and bounces twice in the service box. Effective drop shots require disguise, touch, and the right tactical situation. Best used: when the opponent is deep behind the baseline, when the player has established a strong baseline game, and as a surprise rather than a pattern.",
        "related": ["tactical-tennis", "passing-shots", "approach-shot", "percentage-tennis"],
    },
    {
        "slug": "slice-strategy",
        "title": "The Slice in Modern Tennis",
        "sub_library": "advanced-tennis",
        "summary": "The slice (underspin) is a versatile shot that keeps the ball low, neutralizes pace, and disrupts rhythm. Used on the backhand as a defensive reset, the slice can also be a setup shot. On the forehand, the slice is less common but effective as a change of pace.",
        "related": ["one-handed-backhand-slice", "tactical-tennis", "defensive-strategies", "rhythm-relaxation"],
    },
    {
        "slug": "anticipation-and-reading",
        "title": "Anticipation and Reading the Opponent",
        "sub_library": "advanced-tennis",
        "summary": "Anticipation is reading the opponent's body language, racquet preparation, and contact to predict the shot before it's hit. Elite players read the opponent's shoulders, hips, and racquet face angle to know where the ball is going. Practice: watch the opponent's body, not the ball.",
        "related": ["focus-and-concentration", "tactical-tennis", "split-step", "return-strategy"],
    },

    # ============== SCIENCE OF BIOMECHANICS (8 nodes) ==============
    {
        "slug": "3d-motion-analysis",
        "title": "3D Motion Analysis in Tennis",
        "sub_library": "science-of-biomechanics",
        "summary": "3D motion analysis uses high-speed cameras and reflective markers to capture the exact positions of body segments during tennis strokes. This research has revealed the precise biomechanics of elite serves, groundstrokes, and volleys, providing objective benchmarks for technique. The technology has democratized, with consumer-grade systems now available.",
        "related": ["kinetic-chain", "video-analysis", "ground-reaction-forces", "self-coaching"],
    },
    {
        "slug": "biomechanics-of-serve",
        "title": "Biomechanics of the Tennis Serve",
        "sub_library": "science-of-biomechanics",
        "summary": "The tennis serve is the most complex motion in sports biomechanics. It involves leg drive, hip rotation, shoulder internal rotation, elbow extension, wrist flexion, and pronation—all in less than half a second. The internal shoulder rotation alone can reach 7,000+ degrees per second, the fastest human motion recorded.",
        "related": ["kinetic-chain", "serve-fundamentals", "ground-reaction-forces", "rhythm-relaxation"],
    },
    {
        "slug": "biomechanics-of-forehand",
        "title": "Biomechanics of the Forehand",
        "sub_library": "science-of-biomechanics",
        "summary": "Modern forehand biomechanics emphasize the kinetic chain and hip-shoulder separation. The pelvis rotates approximately 50-70 degrees, the shoulders 100+ degrees, and the arm whips through with racquet head speeds of 80+ mph at elite level. The pronation of the forearm at contact is critical for topspin generation.",
        "related": ["kinetic-chain", "modern-forehand-fundamentals", "open-stance-forehand", "separation-angle"],
    },
    {
        "slug": "biomechanics-of-backhand",
        "title": "Biomechanics of the Backhand",
        "sub_library": "science-of-biomechanics",
        "summary": "The two-handed backhand uses both arms to provide stability against pace, while the one-handed backhand requires more precise timing and strength. The kinetic chain still applies, but the involvement of both arms makes the backhand more stable and powerful for most players. The shoulder rotation is similar to the forehand.",
        "related": ["modern-backhand", "kinetic-chain", "one-handed-backhand-slice", "separation-angle"],
    },
    {
        "slug": "shoulder-injury-prevention",
        "title": "Shoulder Injury Prevention in Tennis",
        "sub_library": "science-of-biomechanics",
        "summary": "Tennis places enormous stress on the shoulder, particularly the rotator cuff. Prevention strategies: proper serving mechanics (avoid arm-only serving), strength training for the rotator cuff and scapular stabilizers, gradual volume increases, and listening to early warning signs. Shoulder injuries often start as fatigue or minor pain.",
        "related": ["biomechanics-of-serve", "kinetic-chain", "rhythm-relaxation", "athletic-development"],
    },
    {
        "slug": "elbow-injury-prevention",
        "title": "Elbow and Tennis Elbow Prevention",
        "sub_library": "science-of-biomechanics",
        "summary": "Tennis elbow (lateral epicondylitis) is common in tennis players. Causes: improper grip pressure, arm-dominant strokes, poor kinetic chain, and overuse. Prevention: develop kinetic chain usage, use appropriate grip pressure, strengthen forearm extensors, and use proper equipment (grip size, racquet weight).",
        "related": ["kinetic-chain", "rhythm-relaxation", "biomechanics-of-forehand", "biomechanics-of-backhand"],
    },
    {
        "slug": "knee-and-hip-mechanics",
        "title": "Knee and Hip Mechanics in Tennis",
        "sub_library": "science-of-biomechanics",
        "summary": "The hip is the powerhouse of tennis movement and stroke generation. Strong hip rotation and stability enable powerful groundstrokes, serves, and movement. The knees absorb landing forces and drive explosive direction changes. Hip and knee injuries are common in tennis, often from sudden direction changes or overuse.",
        "related": ["kinetic-chain", "ground-reaction-forces", "footwork-patterns", "athletic-development"],
    },
    {
        "slug": "grip-pressure",
        "title": "Grip Pressure in Tennis",
        "sub_library": "science-of-biomechanics",
        "summary": "Grip pressure affects both control and power. Too tight a grip restricts wrist action, reduces racquet head speed, and causes forearm fatigue. Too loose a grip causes loss of control. The optimal pressure varies: about 4-5 out of 10 during the swing, briefly squeezing to 6-7 at contact. The continental grip for serves and volleys demands less pressure than the eastern or western grips.",
        "related": ["kinetic-chain", "rhythm-relaxation", "serve-fundamentals", "volley-fundamentals"],
    },

    # ============== HEAVY BALL (4 nodes) ==============
    {
        "slug": "heavy-ball-concept",
        "title": "The Heavy Ball Concept",
        "sub_library": "mysteries-of-the-heavy-ball",
        "summary": "A 'heavy' ball is one that arrives at the opponent with significant pace AND topspin, making it difficult to handle. Heavy balls push opponents back, kick up high, and force defensive replies. Modern players generate heavy balls through proper kinetic chain sequencing, racquet head speed, and low-to-high swing paths.",
        "related": ["lag-mechanics", "kinetic-chain", "topspin-fundamentals", "windshield-wiper"],
    },
    {
        "slug": "ball-speed-data",
        "title": "Ball Speed Data in Pro Tennis",
        "sub_library": "mysteries-of-the-heavy-ball",
        "summary": "Research on professional tennis shows groundstroke speeds averaging 80-90 mph, with the fastest forehands over 100 mph. First serves average 120+ mph at the top level. These speeds have increased steadily over decades due to better technique, equipment, and physical preparation. Recreational players typically hit at 50-70% of professional speeds.",
        "related": ["kinetic-chain", "ground-reaction-forces", "biomechanics-of-forehand", "biomechanics-of-serve"],
    },
    {
        "slug": "spin-rates-and-axes",
        "title": "Spin Rates and Rotation Axes",
        "sub_library": "mysteries-of-the-heavy-ball",
        "summary": "Modern tennis features high spin rates: 2,500-3,500 rpm on top forehands, 4,000+ rpm on kick serves. The axis of rotation matters too: pure topspin spins vertically, slice spins horizontally. The combination of high pace and high spin creates the 'heavy' ball that dominates modern tennis.",
        "related": ["heavy-ball-concept", "topspin-fundamentals", "spin-vs-flat-serve", "kinetic-chain"],
    },
    {
        "slug": "topspin-fundamentals",
        "title": "Topspin Fundamentals",
        "sub_library": "mysteries-of-the-heavy-ball",
        "summary": "Topspin is generated by a low-to-high swing path combined with proper racquet face angle and high racquet head speed. The stringbed grips the ball and rotates it forward. Topspin allows aggressive baseline play with margin over the net, the ball dipping down into the court. Modern racquet technology amplifies spin potential.",
        "related": ["heavy-ball-concept", "kinetic-chain", "windshield-wiper", "spin-rates-and-axes"],
    },

    # ============== TOUR STROKES (4 nodes) ==============
    {
        "slug": "modern-forehand-tour",
        "title": "The Modern Tour Forehand",
        "sub_library": "tour-strokes",
        "summary": "ATP forehands feature extreme grips (semi-western to western), heavy topspin (3,000+ rpm), and open stances. The kinetic chain generates 80+ mph racquet head speed. The windshield wiper finish and pat-the-dog low point are signature characteristics. Modern tour forehands are primarily open-stance, with closed stance used selectively.",
        "related": ["modern-forehand-fundamentals", "open-stance-forehand", "windshield-wiper", "pat-the-dog"],
    },
    {
        "slug": "djokovic-forehand",
        "title": "Djokovic's Defensive Forehand",
        "sub_library": "tour-strokes",
        "summary": "Djokovic's forehand is a study in defensive excellence: extreme flexibility, incredible reach, and consistency under pressure. His stroke uses a semi-western grip, full kinetic chain, and remarkable balance. He generates heavy topspin from defensive positions, turning defense into offense through court positioning and counter-attack patterns.",
        "related": ["modern-forehand-tour", "defensive-strategies", "kinetic-chain", "tactical-tennis"],
    },
    {
        "slug": "medvedev-forehand",
        "title": "Medvedev's Flat Backhand-Defying Forehand",
        "sub_library": "tour-strokes",
        "summary": "Daniil Medvedev's forehand is unique: relatively flat, with a semi-western grip, but used to push opponents back with depth and placement. His unusual contact point and timing make him a nightmare matchup for heavy topspin players. He wins with consistency, depth, and angles rather than pace.",
        "related": ["modern-forehand-tour", "tactical-tennis", "percentage-tennis", "court-positioning"],
    },
    {
        "slug": "tour-serve-analysis",
        "title": "Tour Serve Analysis",
        "sub_library": "tour-strokes",
        "summary": "Modern ATP serves feature extreme variety: 130+ mph first serves, heavy kick second serves, and precise slice serves. Players like Isner, Opelka, and Karlovic use height to generate angle. Others like Federer and Djokovic use variety and placement. The biomechanics involve the full kinetic chain plus extreme internal shoulder rotation.",
        "related": ["biomechanics-of-serve", "serve-fundamentals", "spin-vs-flat-serve", "serve-plus-one"],
    },

    # ============== TENNIS SCIENCE (4 nodes) ==============
    {
        "slug": "anticipating-serves",
        "title": "Anticipating Tennis Serves",
        "sub_library": "tennis-science",
        "summary": "Research on serve anticipation shows elite returners use kinematic cues from the server's body: shoulder rotation, hip position, toss placement, and racquet angle. The best returners start their movement 100-200 ms before the server contacts the ball. Eye tracking studies show experts look at the server's shoulder and hip, not the ball.",
        "related": ["anticipation-and-reading", "return-strategy", "split-step", "focus-and-concentration"],
    },
    {
        "slug": "copoly-strings",
        "title": "Copolyester Strings Explained",
        "sub_library": "tennis-science",
        "summary": "Copolyester (polyester) strings are the modern standard for advanced players. They offer excellent control, durability, and spin potential, but at the cost of power and comfort. Hybrid setups (poly in mains, natural gut or multifilament in crosses) blend poly control with gut feel. String tension affects playability significantly.",
        "related": ["equipment-selection", "kinetic-chain", "rhythm-relaxation", "biomechanics-of-forehand"],
    },
    {
        "slug": "core-strength-tennis",
        "title": "Core Strength for Tennis",
        "sub_library": "tennis-science",
        "summary": "Core strength is fundamental to all tennis strokes and movements. The core transfers power from the lower body to the upper body and stabilizes the spine during rotation. Effective core training includes rotational movements (medicine ball throws, cable rotations), anti-rotation exercises (planks, pallof press), and dynamic stability work.",
        "related": ["athletic-development", "kinetic-chain", "separation-angle", "ground-reaction-forces"],
    },
    {
        "slug": "eccentric-strength",
        "title": "Eccentric Strength in Tennis",
        "sub_library": "tennis-science",
        "summary": "Eccentric strength (muscle lengthening under load) is critical for tennis: decelerating the racquet after contact, controlling landings from jumps, and stabilizing direction changes. Most tennis injuries occur during eccentric phases. Eccentric training (Nordic curls, slow eccentrics) builds resilience and reduces injury risk.",
        "related": ["athletic-development", "biomechanics-of-forehand", "knee-and-hip-mechanics", "shoulder-injury-prevention"],
    },

    # ============== HIGH PERFORMANCE (2 nodes) ==============
    {
        "slug": "shot-tolerance",
        "title": "Shot Tolerance in Elite Tennis",
        "sub_library": "high-performance",
        "summary": "Shot tolerance is the ability to handle extreme pace and spin without breaking down. Elite players develop this through progressive exposure to high-velocity balls, both in practice (with ball machines, hitting partners) and competition. Shot tolerance is built gradually, not overnight, and requires consistent technical foundation.",
        "related": ["kinetic-chain", "biomechanics-of-forehand", "biomechanics-of-backhand", "athletic-development"],
    },
    {
        "slug": "pressure-performance",
        "title": "Performing Under High Pressure",
        "sub_library": "high-performance",
        "summary": "High performance under pressure is the result of preparation, not talent. Players who have done the work in practice perform under pressure; players who haven't, don't. Building pressure performance: simulate pressure in practice, develop consistent routines, embrace pressure as part of the game, and trust the trained stroke.",
        "related": ["mental-toughness", "between-point-routines", "pressure-training", "confidence"],
    },
    # ============== MISC CONCEPTS (cross-cutting) ==============
    {
        "slug": "deliberate-practice",
        "title": "Deliberate Practice",
        "sub_library": "mental-game",
        "summary": "Deliberate practice is focused, structured practice with specific goals and immediate feedback, as opposed to casual repetition. The key elements: clear goals, full concentration, immediate correction, and progressive difficulty. Research shows that deliberate practice, more than innate talent, distinguishes experts from amateurs in any field.",
        "related": ["mental-toughness", "self-coaching", "video-analysis", "muscle-memory", "teaching-progression"],
    },
    {
        "slug": "athletic-development",
        "title": "Athletic Development for Tennis",
        "sub_library": "high-performance",
        "summary": "Tennis-specific athletic development combines strength, power, speed, agility, and flexibility. Key areas: rotational power (medicine ball throws), leg power (jumps, squats), agility (cone drills, ladder), and flexibility (dynamic stretching, yoga). Athletic development reduces injury risk and improves on-court performance.",
        "related": ["kinetic-chain", "ground-reaction-forces", "core-strength-tennis", "eccentric-strength"],
    },
    {
        "slug": "leg-drive",
        "title": "Leg Drive in Tennis Strokes",
        "sub_library": "classic-lessons",
        "summary": "Leg drive is the explosive leg extension that initiates the kinetic chain in serves, groundstrokes, and volleys. Pushing off the ground generates upward and forward force that travels through the body. Without leg drive, strokes are arm-dependent, weaker, and more injury-prone. Even volleys benefit from a small leg push.",
        "related": ["kinetic-chain", "ground-reaction-forces", "open-stance-forehand", "serve-fundamentals"],
    },
    {
        "slug": "defensive-strategies",
        "title": "Defensive Tennis Strategies",
        "sub_library": "advanced-tennis",
        "summary": "Defensive tennis focuses on neutralizing the opponent's offense rather than creating your own. Key tools: high-margin shots, deep depth, slice to reset rhythm, height to buy time, and patient construction. The best defenders like Djokovic and Nadal make opponents play one more ball, accumulating pressure through consistency.",
        "related": ["one-handed-backhand-slice", "percentage-tennis", "court-positioning", "tactical-tennis"],
    },
    {
        "slug": "second-serve-tactics",
        "title": "Second Serve Tactics",
        "sub_library": "strategy-and-statistics",
        "summary": "The second serve is a critical shot in modern tennis, often underrated by amateur players. Tactics: prioritize consistency and depth over pace, use spin to create high bounce (kick serve), and place the serve to set up the third shot. Many amateur points are lost on double faults, so reliability trumps power.",
        "related": ["spin-vs-flat-serve", "serve-fundamentals", "serve-plus-one", "percentage-tennis"],
    },
    {
        "slug": "backhand-biomechanics",
        "title": "Backhand Biomechanics",
        "sub_library": "science-of-biomechanics",
        "summary": "Backhand biomechanics differ from the forehand in that both arms typically drive the swing (two-handed) or the single arm must generate all force with precise timing (one-handed). The kinetic chain still applies, with the hips and shoulders rotating to generate power, but the involvement of both arms changes the stability and timing.",
        "related": ["modern-backhand", "biomechanics-of-backhand", "one-handed-topspin-backhand", "kinetic-chain"],
    },
    {
        "slug": "movement-efficiency",
        "title": "Movement Efficiency in Tennis",
        "sub_library": "footwork",
        "summary": "Movement efficiency means reaching the ball with minimum energy expenditure and maximum balance. Elite players use economy of motion: purposeful first step, efficient mid-court patterns, and quick recovery. Wasted movement (over-running, lazy recovery) costs energy and creates time pressure on every shot.",
        "related": ["footwork-patterns", "split-step", "crossover-step", "recovery-footwork"],
    },
    {
        "slug": "reaction-time",
        "title": "Reaction Time in Tennis",
        "sub_library": "footwork",
        "summary": "Tennis reaction time combines visual processing, decision-making, and physical response. The total reaction time is typically 0.4-0.6 seconds, of which visual processing takes 0.2-0.3 seconds. Reading the opponent early (shoulder, hip, racquet) is the key to faster reaction. Pre-positioning reduces the reaction time needed.",
        "related": ["anticipation-and-reading", "split-step", "first-step", "return-strategy"],
    },
    {
        "slug": "equipment-selection",
        "title": "Tennis Equipment Selection",
        "sub_library": "tennis-science",
        "summary": "Equipment selection affects both performance and injury risk. Key choices: racquet weight (heavier = more control, lighter = more maneuverability), string type (poly = spin, multifilament = comfort, gut = feel), grip size (proper fit reduces elbow strain), and shoes (court-specific, proper fit). Equipment should match the player's level and style.",
        "related": ["copoly-strings", "kinetic-chain", "elbow-injury-prevention", "biomechanics-of-forehand"],
    },
    {
        "slug": "continental-grip",
        "title": "The Continental Grip",
        "sub_library": "ultimate-fundamentals",
        "summary": "The continental grip (also called the 'handshake' grip) is essential for serves, volleys, overheads, and slices. It allows the player to hit balls at various contact points without changing grip. The continental grip is a top-of-handle base knuckle position. Modern teaching emphasizes learning this grip early for versatility.",
        "related": ["serve-fundamentals", "volley-fundamentals", "one-handed-backhand-slice", "kinetic-chain"],
    },
]

# ============================================================
# GENERATE FILES
# ============================================================

print(f"Total concepts: {len(CONCEPTS)}")

# Group by sub-library
from collections import defaultdict
by_sub = defaultdict(list)
for c in CONCEPTS:
    by_sub[c['sub_library']].append(c)

print("\nNodes per sub-library:")
for sub, nodes in by_sub.items():
    print(f"  {sub:35}  {len(nodes)}")

# Generate node files
for c in CONCEPTS:
    sub = c['sub_library']
    node_dir = DST / sub
    node_dir.mkdir(parents=True, exist_ok=True)

    md_lines = ['---']
    md_lines.append(f'title: "{c["title"]}"')
    md_lines.append(f'sub_library: "{sub}"')
    md_lines.append(f'category: "Tennis Knowledgebase"')
    md_lines.append('language: en')
    md_lines.append('vault: tennis-knowledgebase')
    md_lines.append('created: 2026-06-22')
    md_lines.append('updated: 2026-06-22')
    md_lines.append('source_inspiration: "tennisplayer.net teaching library"')
    md_lines.append('content_type: "original synthesis"')
    md_lines.append('---')
    md_lines.append('')
    md_lines.append(f'# {c["title"]}')
    md_lines.append('')
    md_lines.append(c['summary'])
    md_lines.append('')

    if c.get('related'):
        md_lines.append('## Related Concepts')
        md_lines.append('')
        for rel in c['related']:
            # Find the title for this slug
            rel_title = rel.replace('-', ' ').title()
            for other in CONCEPTS:
                if other['slug'] == rel:
                    rel_title = other['title']
                    break
            md_lines.append(f'- [{rel_title}]({rel}.md)')
        md_lines.append('')

    md_lines.append('---')
    md_lines.append('')
    md_lines.append('**Source inspiration:** tennisplayer.net teaching library (John Yandell, 2002-2022) — *not verbatim, this is original synthesis*')
    md_lines.append('')

    out = node_dir / f"{c['slug']}.md"
    out.write_text('\n'.join(md_lines), encoding='utf-8')

print(f"\nGenerated {len(CONCEPTS)} node files")
