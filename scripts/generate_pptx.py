#!/usr/bin/env python3
"""
Q-SHIELD Presentation Generator
Generates presentation-grade PowerPoint deck (10 slides) strictly matching
the official hackathon template from Q-SHIELD.pptx.pdf.
"""

import os
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Slide Dimensions (16:9 Widescreen: 1440 x 810 pt)
SLIDE_WIDTH_PT = 1440
SLIDE_HEIGHT_PT = 810

# Color Palette
BG_COLOR = RGBColor(235, 235, 236)         # #EBEBEC
WHITE = RGBColor(255, 255, 255)            # #FFFFFF
CARD_BG = RGBColor(255, 255, 255)          # #FFFFFF
PILL_PINK = RGBColor(255, 117, 151)        # #FF7597
PILL_TEXT = RGBColor(17, 24, 39)           # #111827
TEXT_TITLE = RGBColor(17, 24, 39)          # #111827
TEXT_SUBTITLE = RGBColor(31, 41, 55)       # #1F2937
TEXT_BODY = RGBColor(55, 65, 81)           # #374151
TEXT_MUTED = RGBColor(107, 114, 128)       # #6B7280
ACCENT_BLUE = RGBColor(29, 78, 216)        # #1D4ED8
ACCENT_CYAN = RGBColor(2, 132, 199)        # #0284C7
ACCENT_GREEN = RGBColor(16, 185, 129)      # #10B981
ACCENT_PURPLE = RGBColor(124, 58, 237)     # #7C3AED
ACCENT_AMBER = RGBColor(245, 158, 11)      # #F59E0B
ACCENT_RED = RGBColor(239, 68, 68)         # #EF4444
BAR_BLUE = RGBColor(79, 134, 198)          # #4F86C6

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "presentation_assets")


def create_blank_slide(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # Base background shape
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(0), Pt(0), Pt(SLIDE_WIDTH_PT), Pt(SLIDE_HEIGHT_PT))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_COLOR
    bg.line.fill.background()

    return slide


def add_footer(slide):
    # Centered footer with pink dot and hackathon label
    footer_box = slide.shapes.add_textbox(Pt(0), Pt(760), Pt(SLIDE_WIDTH_PT), Pt(30))
    tf = footer_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER

    run1 = p.add_run()
    run1.text = "•  "
    run1.font.size = Pt(13)
    run1.font.bold = True
    run1.font.color.rgb = PILL_PINK

    run2 = p.add_run()
    run2.text = "Q-Hack India 2026"
    run2.font.size = Pt(13)
    run2.font.bold = True
    run2.font.color.rgb = TEXT_TITLE

    run3 = p.add_run()
    run3.text = "  •"
    run3.font.size = Pt(13)
    run3.font.bold = True
    run3.font.color.rgb = PILL_PINK


def add_standard_header(slide, pill_text, heading_text):
    # Top Left: Quantum Week 26
    qw_logo = os.path.join(ASSETS_DIR, "logo_quantum_week.png")
    if os.path.exists(qw_logo):
        slide.shapes.add_picture(qw_logo, Pt(35), Pt(25), width=Pt(210))

    # Top Center: RIT icon
    rit_logo = os.path.join(ASSETS_DIR, "logo_rit.png")
    if os.path.exists(rit_logo):
        slide.shapes.add_picture(rit_logo, Pt(695), Pt(22), width=Pt(50))

    # Top Right: IBM Quantum
    ibm_logo = os.path.join(ASSETS_DIR, "logo_ibm_quantum.png")
    if os.path.exists(ibm_logo):
        slide.shapes.add_picture(ibm_logo, Pt(1110), Pt(32), width=Pt(260))

    # Center Pill Badge
    pill_w = max(220, len(pill_text) * 16)
    pill_x = (SLIDE_WIDTH_PT - pill_w) / 2
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(pill_x), Pt(142), Pt(pill_w), Pt(48))
    pill.fill.solid()
    pill.fill.fore_color.rgb = PILL_PINK
    pill.line.fill.background()
    tf_pill = pill.text_frame
    tf_pill.word_wrap = False
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = pill_text
    p_pill.font.size = Pt(18)
    p_pill.font.bold = True
    p_pill.font.color.rgb = PILL_TEXT
    p_pill.alignment = PP_ALIGN.CENTER

    # Main Heading
    head_box = slide.shapes.add_textbox(Pt(100), Pt(210), Pt(1240), Pt(65))
    tf_head = head_box.text_frame
    tf_head.word_wrap = True
    p_head = tf_head.paragraphs[0]
    p_head.text = heading_text
    p_head.font.size = Pt(32)
    p_head.font.bold = True
    p_head.font.color.rgb = TEXT_TITLE
    p_head.alignment = PP_ALIGN.CENTER

    # Mascot Bird in bottom right
    mascot = os.path.join(ASSETS_DIR, "mascot_bird_corner.png")
    if os.path.exists(mascot):
        slide.shapes.add_picture(mascot, Pt(1300), Pt(640), width=Pt(110))

    add_footer(slide)


def add_white_card(slide, x, y, w, h):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(x), Pt(y), Pt(w), Pt(h))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.fill.background()
    return card


# ==============================================================================
# Slide 1: Title & Overview
# ==============================================================================
def build_slide_1(prs):
    slide = create_blank_slide(prs)

    # Top logos row
    ram_logo = os.path.join(ASSETS_DIR, "logo_ramaiah.png")
    if os.path.exists(ram_logo):
        slide.shapes.add_picture(ram_logo, Pt(35), Pt(32), width=Pt(270))

    ieee_logo = os.path.join(ASSETS_DIR, "logo_ieeecis.png")
    if os.path.exists(ieee_logo):
        slide.shapes.add_picture(ieee_logo, Pt(360), Pt(22), width=Pt(170))

    rit_logo = os.path.join(ASSETS_DIR, "logo_rit.png")
    if os.path.exists(rit_logo):
        slide.shapes.add_picture(rit_logo, Pt(620), Pt(32), width=Pt(55))

    qw_logo = os.path.join(ASSETS_DIR, "logo_quantum_week.png")
    if os.path.exists(qw_logo):
        slide.shapes.add_picture(qw_logo, Pt(760), Pt(32), width=Pt(210))

    ibm_logo = os.path.join(ASSETS_DIR, "logo_ibm_quantum.png")
    if os.path.exists(ibm_logo):
        slide.shapes.add_picture(ibm_logo, Pt(1070), Pt(42), width=Pt(270))

    # Center Q-Hack India 2026 Cryostat Logo
    qhack_logo = os.path.join(ASSETS_DIR, "logo_qhack_2026.png")
    if os.path.exists(qhack_logo):
        slide.shapes.add_picture(qhack_logo, Pt(450), Pt(135), width=Pt(410))

    # Left-side Pill Metadata
    pills_data = [
        ("Team Name:", 230, 310),
        ("Team Lead Name:", 310, 380),
        ("Track:", 170, 445),
        ("Problem Statement title:", 390, 510),
    ]
    for text, w, y in pills_data:
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(40), Pt(y), Pt(w), Pt(44))
        pill.fill.solid()
        pill.fill.fore_color.rgb = PILL_PINK
        pill.line.fill.background()
        tf = pill.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = PILL_TEXT
        p.alignment = PP_ALIGN.CENTER

    # Project Title & Subtitle
    title_box = slide.shapes.add_textbox(Pt(40), Pt(585), Pt(840), Pt(65))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = "Q-SHIELD: End-to-End Quantum Security Platform"
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(30, 27, 75)

    sub_box = slide.shapes.add_textbox(Pt(40), Pt(655), Pt(840), Pt(50))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Discover, understand, protect, and migrate quantum-vulnerable cryptography before Q-day"
    p_sub.font.size = Pt(16)
    p_sub.font.bold = False
    p_sub.font.color.rgb = TEXT_BODY

    # Right-side Hero Illustration
    hero_img = os.path.join(ASSETS_DIR, "hero_illustration.png")
    if os.path.exists(hero_img):
        slide.shapes.add_picture(hero_img, Pt(920), Pt(210), width=Pt(435))

    add_footer(slide)


# ==============================================================================
# Slide 2: Problem
# ==============================================================================
def build_slide_2(prs):
    slide = create_blank_slide(prs)
    add_standard_header(slide, "Problem", "Today's public-key cryptography has an expiry date")

    cards_data = [
        (
            1,
            "Shor breaks RSA & ECC",
            "A large fault-tolerant quantum computer running Shor's algorithm derives private keys from public keys in polynomial time. RSA, ECDSA, ECDH, and Diffie-Hellman all fall.",
            85,
        ),
        (
            2,
            "Harvest now, decrypt later",
            "Attackers record encrypted network traffic and exfiltrate ciphertext today to decrypt once quantum hardware scales. Long-lived financial, healthcare, and state records are exposed already.",
            520,
        ),
        (
            3,
            "No inventory, no plan",
            "Most organizations lack visibility into where vulnerable algorithms live across polyglot repositories, configurations, and certificates, making multi-year migrations difficult to sequence.",
            955,
        ),
    ]

    for num, title, body, x in cards_data:
        add_white_card(slide, x, 290, 400, 350)

        # Number circle
        circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(x + 24), Pt(314), Pt(52), Pt(52))
        circ.fill.solid()
        circ.fill.fore_color.rgb = PILL_PINK
        circ.line.fill.background()
        tf_c = circ.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.text = str(num)
        p_c.font.size = Pt(20)
        p_c.font.bold = True
        p_c.font.color.rgb = RGBColor(0, 0, 0)
        p_c.alignment = PP_ALIGN.CENTER

        # Card Title
        tb_t = slide.shapes.add_textbox(Pt(x + 24), Pt(385), Pt(352), Pt(50))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(21)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_TITLE

        # Card Body
        tb_b = slide.shapes.add_textbox(Pt(x + 24), Pt(450), Pt(352), Pt(175))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        p_b = tf_b.paragraphs[0]
        p_b.text = body
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = TEXT_BODY

    # Regulatory footer note
    fn_box = slide.shapes.add_textbox(Pt(85), Pt(670), Pt(1270), Pt(45))
    tf_fn = fn_box.text_frame
    tf_fn.word_wrap = True
    p_fn = tf_fn.paragraphs[0]
    p_fn.text = "The clock is set: NIST standardized ML-KEM, ML-DSA, and SLH-DSA in August 2024 (FIPS 203–205) and plans to deprecate quantum-vulnerable public-key algorithms after 2030 (NIST IR 8547)."
    p_fn.font.size = Pt(13)
    p_fn.font.bold = True
    p_fn.font.color.rgb = TEXT_TITLE


# ==============================================================================
# Slide 3: Why It Matters (Mosca Inequality)
# ==============================================================================
def build_slide_3(prs):
    slide = create_blank_slide(prs)
    add_standard_header(slide, "Why It Matters", "The deadline is set by your data, not by quantum computers")

    # Left Column: Who faces it
    add_white_card(slide, 85, 290, 560, 420)

    tb_w_t = slide.shapes.add_textbox(Pt(115), Pt(310), Pt(500), Pt(40))
    p_w_t = tb_w_t.text_frame.paragraphs[0]
    p_w_t.text = "Who faces it"
    p_w_t.font.size = Pt(22)
    p_w_t.font.bold = True
    p_w_t.font.color.rgb = TEXT_TITLE

    sectors = [
        ("1", "Banks & payments", "transaction records, card data, inter-bank clearing keys"),
        ("2", "Healthcare", "medical records and genomic data kept for decades"),
        ("3", "Government & defense", "classified intelligence, citizen identity registries"),
        ("4", "Any organization", "proprietary data that must stay secret for 10+ years"),
    ]

    for i, (num, name, desc) in enumerate(sectors):
        y_pos = 365 + i * 82
        circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(115), Pt(y_pos), Pt(36), Pt(36))
        circ.fill.solid()
        circ.fill.fore_color.rgb = PILL_PINK
        circ.line.fill.background()
        tf_c = circ.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.text = num
        p_c.font.size = Pt(15)
        p_c.font.bold = True
        p_c.font.color.rgb = RGBColor(0, 0, 0)
        p_c.alignment = PP_ALIGN.CENTER

        tb_s = slide.shapes.add_textbox(Pt(165), Pt(y_pos - 4), Pt(450), Pt(70))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        p_s_n = tf_s.paragraphs[0]
        p_s_n.text = name
        p_s_n.font.size = Pt(16)
        p_s_n.font.bold = True
        p_s_n.font.color.rgb = TEXT_TITLE

        p_s_d = tf_s.add_paragraph()
        p_s_d.text = desc
        p_s_d.font.size = Pt(13)
        p_s_d.font.color.rgb = TEXT_MUTED

    # Right Column: Mosca's Inequality
    add_white_card(slide, 675, 290, 680, 420)

    tb_m_t = slide.shapes.add_textbox(Pt(705), Pt(310), Pt(620), Pt(40))
    p_m_t = tb_m_t.text_frame.paragraphs[0]
    p_m_t.text = "Mosca's inequality: data is at risk when"
    p_m_t.font.size = Pt(20)
    p_m_t.font.bold = True
    p_m_t.font.color.rgb = TEXT_TITLE

    # Big Equation Box
    eq_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(705), Pt(355), Pt(620), Pt(68))
    eq_box.fill.solid()
    eq_box.fill.fore_color.rgb = RGBColor(243, 244, 246)
    eq_box.line.color.rgb = RGBColor(229, 231, 235)
    tf_eq = eq_box.text_frame
    p_eq = tf_eq.paragraphs[0]
    p_eq.text = "X  +  Y  >  Z"
    p_eq.font.size = Pt(30)
    p_eq.font.bold = True
    p_eq.font.color.rgb = ACCENT_RED
    p_eq.alignment = PP_ALIGN.CENTER

    tb_def = slide.shapes.add_textbox(Pt(705), Pt(430), Pt(620), Pt(30))
    p_def = tb_def.text_frame.paragraphs[0]
    p_def.text = "X = years data must stay secret  ·  Y = years to migrate  ·  Z = years until Q-day"
    p_def.font.size = Pt(13)
    p_def.font.bold = True
    p_def.font.color.rgb = TEXT_MUTED
    p_def.alignment = PP_ALIGN.CENTER

    # Example from scan
    tb_ex_t = slide.shapes.add_textbox(Pt(705), Pt(475), Pt(620), Pt(30))
    p_ex_t = tb_ex_t.text_frame.paragraphs[0]
    p_ex_t.text = "Example from our scan: QuantumBank payment-api"
    p_ex_t.font.size = Pt(16)
    p_ex_t.font.bold = True
    p_ex_t.font.color.rgb = TEXT_TITLE

    # Three metric pill chips
    chips = [
        ("records kept: 10 y", 705, ACCENT_AMBER),
        ("migrate: 2.3 y", 920, ACCENT_AMBER),
        ("Q-day ≈ 12 y", 1135, ACCENT_CYAN),
    ]
    for c_text, c_x, c_col in chips:
        c_shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(c_x), Pt(515), Pt(190), Pt(42))
        c_shp.fill.solid()
        c_shp.fill.fore_color.rgb = RGBColor(243, 244, 246)
        c_shp.line.color.rgb = c_col
        tf_c = c_shp.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.text = c_text
        p_c.font.size = Pt(14)
        p_c.font.bold = True
        p_c.font.color.rgb = TEXT_TITLE
        p_c.alignment = PP_ALIGN.CENTER

    # Result statement box
    res_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(705), Pt(580), Pt(620), Pt(105))
    res_box.fill.solid()
    res_box.fill.fore_color.rgb = RGBColor(254, 242, 242)
    res_box.line.color.rgb = RGBColor(254, 202, 202)
    tf_res = res_box.text_frame
    tf_res.word_wrap = True
    p_res = tf_res.paragraphs[0]
    p_res.text = "Result: 10.0 + 2.3 = 12.3 y > 12.0 y (Q-day)"
    p_res.font.size = Pt(15)
    p_res.font.bold = True
    p_res.font.color.rgb = ACCENT_RED

    p_res_b = tf_res.add_paragraph()
    p_res_b.text = "RSA-protected financial records outlive their encryption today, rated high exposure. Migration has to start now."
    p_res_b.font.size = Pt(13)
    p_res_b.font.color.rgb = TEXT_BODY


# ==============================================================================
# Slide 4: Proposed Solution
# ==============================================================================
def build_slide_4(prs):
    slide = create_blank_slide(prs)
    add_standard_header(slide, "Proposed Solution", "One platform from discovery to migration")

    pillars = [
        (
            1,
            "DISCOVER",
            "Crypto scanner",
            "Scans Python, Java, JS and Go code, SSH/JWT configs, X.509 certificates and committed keys into a Cryptographic Bill of Materials.",
            85,
        ),
        (
            2,
            "UNDERSTAND",
            "Risk + quantum threat",
            "Readiness score 0–100, harvest-now-decrypt-later exposure per data class, Shor and Grover simulated.",
            405,
        ),
        (
            3,
            "PROTECT",
            "PQC gateway",
            "Quantum-safe channel with ML-KEM-768 key exchange and ML-DSA-65 signatures, hybrid with X25519.",
            725,
        ),
        (
            4,
            "MIGRATE",
            "Crypto-agility engine",
            "A replacement for every finding, a 4-phase roadmap and the projected readiness after each phase.",
            1045,
        ),
    ]

    for num, tag, title, body, x in pillars:
        add_white_card(slide, x, 285, 305, 335)

        # Number circle + tag
        circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(x + 18), Pt(305), Pt(40), Pt(40))
        circ.fill.solid()
        circ.fill.fore_color.rgb = PILL_PINK
        circ.line.fill.background()
        tf_c = circ.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.text = str(num)
        p_c.font.size = Pt(17)
        p_c.font.bold = True
        p_c.font.color.rgb = RGBColor(0, 0, 0)
        p_c.alignment = PP_ALIGN.CENTER

        tb_tag = slide.shapes.add_textbox(Pt(x + 68), Pt(312), Pt(210), Pt(30))
        p_tag = tb_tag.text_frame.paragraphs[0]
        p_tag.text = tag
        p_tag.font.size = Pt(14)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_CYAN

        tb_t = slide.shapes.add_textbox(Pt(x + 18), Pt(360), Pt(270), Pt(45))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(19)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_TITLE

        tb_b = slide.shapes.add_textbox(Pt(x + 18), Pt(420), Pt(270), Pt(180))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        p_b = tf_b.paragraphs[0]
        p_b.text = body
        p_b.font.size = Pt(13)
        p_b.font.color.rgb = TEXT_BODY

    # Pillar 5: Bottom AI Copilot Bar
    bar = add_white_card(slide, 85, 638, 1265, 80)
    tb_c = slide.shapes.add_textbox(Pt(105), Pt(648), Pt(1225), Pt(60))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]

    r_num = p_c.add_run()
    r_num.text = "5  "
    r_num.font.size = Pt(18)
    r_num.font.bold = True
    r_num.font.color.rgb = PILL_PINK

    r_lbl = p_c.add_run()
    r_lbl.text = "AI SECURITY COPILOT:  "
    r_lbl.font.size = Pt(16)
    r_lbl.font.bold = True
    r_lbl.font.color.rgb = TEXT_TITLE

    r_desc = p_c.add_run()
    r_desc.text = "Explains the risk, answers \"what should we migrate first?\", writes developer tickets and an executive audit report, strictly grounded in verified CBOM finding IDs."
    r_desc.font.size = Pt(14)
    r_desc.font.color.rgb = TEXT_BODY


# ==============================================================================
# Slide 5: Why Quantum?
# ==============================================================================
def build_slide_5(prs):
    slide = create_blank_slide(prs)
    add_standard_header(slide, "Why Quantum?", "Quantum computing is both the threat and our method")

    # Left: The threat
    add_white_card(slide, 85, 280, 610, 185)

    tb_t_t = slide.shapes.add_textbox(Pt(105), Pt(295), Pt(570), Pt(35))
    p_t_t = tb_t_t.text_frame.paragraphs[0]
    p_t_t.text = "The threat"
    p_t_t.font.size = Pt(18)
    p_t_t.font.bold = True
    p_t_t.font.color.rgb = TEXT_TITLE

    # Shor item
    tb_shor = slide.shapes.add_textbox(Pt(105), Pt(335), Pt(570), Pt(60))
    tf_shor = tb_shor.text_frame
    tf_shor.word_wrap = True
    p_s = tf_shor.paragraphs[0]
    r_sn = p_s.add_run()
    r_sn.text = "Shor's algorithm  "
    r_sn.font.bold = True
    r_sn.font.size = Pt(14)

    r_sb = p_s.add_run()
    r_sb.text = "[ Broken ]\n"
    r_sb.font.bold = True
    r_sb.font.size = Pt(12)
    r_sb.font.color.rgb = ACCENT_RED

    r_sd = p_s.add_run()
    r_sd.text = "Exponential speedup for factoring and discrete logarithms: RSA and elliptic-curve keys can be derived from public keys."
    r_sd.font.size = Pt(12)
    r_sd.font.color.rgb = TEXT_BODY

    # Grover item
    tb_grover = slide.shapes.add_textbox(Pt(105), Pt(395), Pt(570), Pt(60))
    tf_grover = tb_grover.text_frame
    tf_grover.word_wrap = True
    p_g = tf_grover.paragraphs[0]
    r_gn = p_g.add_run()
    r_gn.text = "Grover's algorithm  "
    r_gn.font.bold = True
    r_gn.font.size = Pt(14)

    r_gb = p_g.add_run()
    r_gb.text = "[ Weakened ]\n"
    r_gb.font.bold = True
    r_gb.font.size = Pt(12)
    r_gb.font.color.rgb = ACCENT_AMBER

    r_gd = p_g.add_run()
    r_gd.text = "Quadratic speedup for brute-force search: AES-128 drops to about 64-bit strength; AES-256 keeps 128 bits."
    r_gd.font.size = Pt(12)
    r_gd.font.color.rgb = TEXT_BODY

    # Right: Our method
    add_white_card(slide, 720, 280, 630, 185)

    tb_m_t = slide.shapes.add_textbox(Pt(740), Pt(295), Pt(590), Pt(35))
    p_m_t = tb_m_t.text_frame.paragraphs[0]
    p_m_t.text = "Our method"
    p_m_t.font.size = Pt(18)
    p_m_t.font.bold = True
    p_m_t.font.color.rgb = TEXT_TITLE

    tb_m_b = slide.shapes.add_textbox(Pt(740), Pt(335), Pt(590), Pt(120))
    tf_m_b = tb_m_b.text_frame
    tf_m_b.word_wrap = True
    p_mb = tf_m_b.paragraphs[0]
    p_mb.text = "Exact statevector simulation of Shor's period finding: modular exponentiation f(x) = a^x mod N, inverse QFT, measurement, then continued fractions and gcd.\n\nPost-quantum ML-KEM and ML-DSA are built on lattice problems that resist this adversary because they lack periodic abelian structure."
    p_mb.font.size = Pt(13)
    p_mb.font.color.rgb = TEXT_BODY

    # Bottom: Shor Simulation Chart
    add_white_card(slide, 85, 480, 1265, 235)

    tb_c_t = slide.shapes.add_textbox(Pt(115), Pt(495), Pt(1200), Pt(35))
    p_ct = tb_c_t.text_frame.paragraphs[0]
    p_ct.text = "Shor simulation, N = 15, a = 7: peaks occur every Q/r = 64 (s in {0, 64, 128, 192})"
    p_ct.font.size = Pt(16)
    p_ct.font.bold = True
    p_ct.font.color.rgb = TEXT_TITLE

    # Draw simulated peak bars
    axis_y = 660
    base_x = 220
    spacing = 240

    # Draw axis line
    axis = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(base_x - 30), Pt(axis_y), Pt(1000), Pt(2))
    axis.fill.solid()
    axis.fill.fore_color.rgb = RGBColor(209, 213, 219)
    axis.line.fill.background()

    # Draw 4 main peaks at 0, 64, 128, 192, 256
    peak_states = [("0", 0), ("64", 1), ("128", 2), ("192", 3), ("256", 4)]
    for lbl, idx in peak_states:
        px = base_x + idx * spacing
        # Bar shape
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(px - 10), Pt(axis_y - 100), Pt(20), Pt(100))
        bar.fill.solid()
        bar.fill.fore_color.rgb = ACCENT_PURPLE
        bar.line.fill.background()

        # State label
        lbl_box = slide.shapes.add_textbox(Pt(px - 30), Pt(axis_y + 6), Pt(60), Pt(25))
        p_l = lbl_box.text_frame.paragraphs[0]
        p_l.text = lbl
        p_l.font.size = Pt(11)
        p_l.font.bold = True
        p_l.font.color.rgb = TEXT_MUTED
        p_l.alignment = PP_ALIGN.CENTER

        # Probability label
        p_box = slide.shapes.add_textbox(Pt(px - 35), Pt(axis_y - 126), Pt(70), Pt(25))
        p_prob = p_box.text_frame.paragraphs[0]
        p_prob.text = "P=0.25"
        p_prob.font.size = Pt(11)
        p_prob.font.bold = True
        p_prob.font.color.rgb = ACCENT_PURPLE
        p_prob.alignment = PP_ALIGN.CENTER


# ==============================================================================
# Slide 6: Implementation & Architecture
# ==============================================================================
def build_slide_6(prs):
    slide = create_blank_slide(prs)
    add_standard_header(slide, "Implementation and Architecture", "One inventory feeds every module")

    # Inputs Box
    add_white_card(slide, 85, 280, 240, 360)
    tb_in_t = slide.shapes.add_textbox(Pt(105), Pt(295), Pt(200), Pt(35))
    p_in_t = tb_in_t.text_frame.paragraphs[0]
    p_in_t.text = "Inputs"
    p_in_t.font.size = Pt(18)
    p_in_t.font.bold = True
    p_in_t.font.color.rgb = TEXT_TITLE

    inputs_list = [
        "• Git repository URL",
        "• ZIP archive upload",
        "• Polyglot source code",
        "• Server configurations",
        "• Certificates & keys",
    ]
    tb_in_b = slide.shapes.add_textbox(Pt(105), Pt(340), Pt(200), Pt(280))
    tf_in = tb_in_b.text_frame
    for item in inputs_list:
        p = tf_in.add_paragraph()
        p.text = item
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_BODY

    # Middle: FastAPI Backend Engine
    add_white_card(slide, 345, 280, 600, 360)
    tb_mid_t = slide.shapes.add_textbox(Pt(365), Pt(295), Pt(560), Pt(35))
    p_mid_t = tb_mid_t.text_frame.paragraphs[0]
    p_mid_t.text = "FastAPI backend (Python)"
    p_mid_t.font.size = Pt(18)
    p_mid_t.font.bold = True
    p_mid_t.font.color.rgb = TEXT_TITLE

    modules = [
        ("Crypto scanner", ACCENT_CYAN, "Polyglot static analysis with comment stripping"),
        ("Risk engine", ACCENT_AMBER, "Mosca inequality & Grover degradation calculation"),
        ("Quantum simulator", ACCENT_PURPLE, "Exact statevector Shor & multi-qubit circuits"),
        ("PQC gateway", ACCENT_GREEN, "Hybrid ML-KEM-768 + ML-DSA-65 channel"),
        ("Migration engine", ACCENT_BLUE, "Contextual code replacement diff generator"),
        ("AI copilot", RGBColor(234, 179, 8), "Grounded advisor validated against SQLite CBOM"),
    ]
    for i, (mod_name, col, mod_desc) in enumerate(modules):
        mx = 365 + (i % 2) * 280
        my = 345 + (i // 2) * 75
        m_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(mx), Pt(my), Pt(265), Pt(65))
        m_card.fill.solid()
        m_card.fill.fore_color.rgb = RGBColor(243, 244, 246)
        m_card.line.color.rgb = col
        tf_m = m_card.text_frame
        p_mn = tf_m.paragraphs[0]
        p_mn.text = mod_name
        p_mn.font.size = Pt(13)
        p_mn.font.bold = True
        p_mn.font.color.rgb = TEXT_TITLE

        p_md = tf_m.add_paragraph()
        p_md.text = mod_desc
        p_md.font.size = Pt(10)
        p_md.font.color.rgb = TEXT_MUTED

    # Bottom strip inside mid: CBOM + SQLite
    cbom_strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(365), Pt(580), Pt(560), Pt(42))
    cbom_strip.fill.solid()
    cbom_strip.fill.fore_color.rgb = RGBColor(238, 242, 255)
    cbom_strip.line.color.rgb = ACCENT_BLUE
    p_cs = cbom_strip.text_frame.paragraphs[0]
    p_cs.text = "Cryptographic Bill of Materials (CycloneDX 1.6 Schema) · SQLite"
    p_cs.font.size = Pt(12)
    p_cs.font.bold = True
    p_cs.font.color.rgb = ACCENT_BLUE
    p_cs.alignment = PP_ALIGN.CENTER

    # Right: Outputs
    add_white_card(slide, 965, 280, 385, 360)
    tb_out_t = slide.shapes.add_textbox(Pt(985), Pt(295), Pt(345), Pt(35))
    p_out_t = tb_out_t.text_frame.paragraphs[0]
    p_out_t.text = "Outputs"
    p_out_t.font.size = Pt(18)
    p_out_t.font.bold = True
    p_out_t.font.color.rgb = TEXT_TITLE

    outputs_list = [
        "• Guided console (5 stages / 7 tabs)",
        "• Quantum-safe encrypted channel",
        "• Executive risk audit report (Markdown)",
        "• Developer tickets (Jira / GitHub)",
        "• Machine-readable CBOM export (JSON)",
    ]
    tb_out_b = slide.shapes.add_textbox(Pt(985), Pt(340), Pt(345), Pt(280))
    tf_out = tb_out_b.text_frame
    for item in outputs_list:
        p = tf_out.add_paragraph()
        p.text = item
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_BODY

    # Bottom Stack Summary
    stack_box = add_white_card(slide, 85, 655, 1265, 62)
    tb_st = slide.shapes.add_textbox(Pt(105), Pt(662), Pt(1225), Pt(50))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True
    p_st = tf_st.paragraphs[0]
    p_st.text = "Stack: Python · FastAPI · pyca/cryptography (OpenSSL 3.5) for ML-KEM-768, ML-DSA-65, AES-256-GCM · NumPy statevector · SQLite · Plain JS + SVG · Docker"
    p_st.font.size = Pt(13)
    p_st.font.bold = True
    p_st.font.color.rgb = TEXT_TITLE
    p_st.alignment = PP_ALIGN.CENTER


# ==============================================================================
# Slide 7: Minimal Prototype
# ==============================================================================
def build_slide_7(prs):
    slide = create_blank_slide(prs)
    add_standard_header(slide, "Minimal Prototype", "A working platform, not a mock-up")

    # Main Left Card: Overview Screenshot
    add_white_card(slide, 85, 275, 650, 440)
    screen_ov = os.path.join(ASSETS_DIR, "screen_overview.png")
    if os.path.exists(screen_ov):
        slide.shapes.add_picture(screen_ov, Pt(95), Pt(285), width=Pt(630))
    tb_ov_cap = slide.shapes.add_textbox(Pt(95), Pt(680), Pt(630), Pt(30))
    p_ov_c = tb_ov_cap.text_frame.paragraphs[0]
    p_ov_c.text = "Overview: scan of QuantumBank, 27 assets cataloged, readiness evaluated at 33/100"
    p_ov_c.font.size = Pt(12)
    p_ov_c.font.bold = True
    p_ov_c.font.color.rgb = TEXT_TITLE

    # 4 Quadrant Screenshots on Right
    quads = [
        ("screen_shor.png", "Shor simulation on 143", 755, 275),
        ("screen_pqc.png", "ML-KEM chat, tamper rejected", 1060, 275),
        ("screen_roadmap.png", "Roadmap: 33 → 84 → 96", 755, 495),
        ("screen_copilot.png", "Grounded AI copilot", 1060, 495),
    ]

    for f_name, cap, qx, qy in quads:
        add_white_card(slide, qx, qy, 290, 220)
        img_p = os.path.join(ASSETS_DIR, f_name)
        if os.path.exists(img_p):
            slide.shapes.add_picture(img_p, Pt(qx + 8), Pt(qy + 8), width=Pt(274))
        tb_q = slide.shapes.add_textbox(Pt(qx + 8), Pt(qy + 185), Pt(274), Pt(30))
        p_qc = tb_q.text_frame.paragraphs[0]
        p_qc.text = cap
        p_qc.font.size = Pt(11)
        p_qc.font.bold = True
        p_qc.font.color.rgb = TEXT_TITLE
        p_qc.alignment = PP_ALIGN.CENTER


# ==============================================================================
# Slide 8: Results & Validation
# ==============================================================================
def build_slide_8(prs):
    slide = create_blank_slide(prs)
    add_standard_header(slide, "Results / Validation", "Validated on a seeded bank, end to end")

    # Top 4 Metric Cards
    top_metrics = [
        (
            "27 / 27",
            "seeded crypto assets found in QuantumBank, 0 hits on commented-out code or docs",
            85,
            ACCENT_CYAN,
        ),
        (
            "33 → 84",
            "readiness after roadmap phases 1–3 (96 after phase 4), recomputed by the risk engine",
            405,
            ACCENT_AMBER,
        ),
        (
            "8,954 B",
            "hybrid ML-KEM-768 + ML-DSA-65 handshake, a few ms of compute",
            725,
            ACCENT_PURPLE,
        ),
        (
            "84",
            "automated tests passing, including tamper, replay and MITM rejection",
            1045,
            ACCENT_GREEN,
        ),
    ]

    for val, label, x, col in top_metrics:
        add_white_card(slide, x, 275, 305, 175)

        tb_v = slide.shapes.add_textbox(Pt(x + 15), Pt(290), Pt(275), Pt(55))
        p_v = tb_v.text_frame.paragraphs[0]
        p_v.text = val
        p_v.font.size = Pt(36)
        p_v.font.bold = True
        p_v.font.color.rgb = col

        tb_l = slide.shapes.add_textbox(Pt(x + 15), Pt(350), Pt(275), Pt(90))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True
        p_l = tf_l.paragraphs[0]
        p_l.text = label
        p_l.font.size = Pt(13)
        p_l.font.color.rgb = TEXT_BODY

    # Bottom Left: Readiness Bar Chart Card
    add_white_card(slide, 85, 470, 580, 245)
    tb_bc_t = slide.shapes.add_textbox(Pt(105), Pt(485), Pt(540), Pt(30))
    p_bct = tb_bc_t.text_frame.paragraphs[0]
    p_bct.text = "Quantum Readiness by roadmap phase (QuantumBank)"
    p_bct.font.size = Pt(14)
    p_bct.font.bold = True
    p_bct.font.color.rgb = TEXT_TITLE

    # Draw Chart Bars
    chart_y_base = 675
    chart_x_base = 140
    chart_spacing = 95
    bars_data = [
        ("Today", 33.0, 33),
        ("Phase 1", 42.0, 42),
        ("Phase 2", 55.0, 55),
        ("Phase 3", 84.0, 84),
        ("Phase 4", 96.0, 96),
    ]

    for label, val, score in bars_data:
        bx = chart_x_base + bars_data.index((label, val, score)) * chart_spacing
        b_height = int(score * 1.5)

        # Bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Pt(bx), Pt(chart_y_base - b_height), Pt(50), Pt(b_height))
        bar.fill.solid()
        bar.fill.fore_color.rgb = BAR_BLUE
        bar.line.fill.background()

        # Score label on top of bar
        s_box = slide.shapes.add_textbox(Pt(bx - 10), Pt(chart_y_base - b_height - 24), Pt(70), Pt(24))
        p_s = s_box.text_frame.paragraphs[0]
        p_s.text = f"{val:.1f}"
        p_s.font.size = Pt(10)
        p_s.font.bold = True
        p_s.font.color.rgb = TEXT_TITLE
        p_s.alignment = PP_ALIGN.CENTER

        # Stage label below bar
        l_box = slide.shapes.add_textbox(Pt(bx - 15), Pt(chart_y_base + 6), Pt(80), Pt(24))
        p_lbl = l_box.text_frame.paragraphs[0]
        p_lbl.text = label
        p_lbl.font.size = Pt(11)
        p_lbl.font.color.rgb = TEXT_MUTED
        p_lbl.alignment = PP_ALIGN.CENTER

    # Bottom Right: Also validated Card
    add_white_card(slide, 685, 470, 665, 245)
    tb_av_t = slide.shapes.add_textbox(Pt(710), Pt(485), Pt(620), Pt(30))
    p_avt = tb_av_t.text_frame.paragraphs[0]
    p_avt.text = "Also validated"
    p_avt.font.size = Pt(16)
    p_avt.font.bold = True
    p_avt.font.color.rgb = TEXT_TITLE

    av_items = [
        "• Shor simulation factors 15, 21, 143, 221 and 247; peaks match theory exactly",
        "• ML-KEM/ML-DSA wire sizes match FIPS 203/204 (1184 B key, 1088 B ciphertext, 3309 B signature)",
        "• Copilot cites only real finding IDs; invented IDs are flagged and rejected",
        "• ZIP-slip archives and unsafe Git URLs rejected",
    ]
    tb_av_b = slide.shapes.add_textbox(Pt(710), Pt(525), Pt(620), Pt(175))
    tf_av = tb_av_b.text_frame
    for item in av_items:
        p = tf_av.add_paragraph()
        p.text = item
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_BODY


# ==============================================================================
# Slide 9: Roadmap
# ==============================================================================
def build_slide_9(prs):
    slide = create_blank_slide(prs)
    add_standard_header(slide, "Roadmap", "From demo app to real codebases")

    roadmap_cols = [
        (
            1,
            "Deeper discovery",
            [
                "• AST and data-flow analysis",
                "• Binaries and container images",
                "• Live TLS/SSH endpoint scanning",
            ],
            85,
        ),
        (
            2,
            "Standards & CI",
            [
                "• CycloneDX CBOM export",
                "• CI gate blocking vulnerable crypto",
                "• Automated GitHub app remediation",
            ],
            405,
        ),
        (
            3,
            "Production PQC",
            [
                "• Hybrid TLS gateway (X25519MLKEM768)",
                "• Post-quantum / composite certificates",
                "• Cloud KMS and HSM integration",
            ],
            725,
        ),
        (
            4,
            "Real validation",
            [
                "• Precision/recall on public repos",
                "• Enterprise pilot with a partner bank",
                "• Shor N = 15 on IBM Quantum hardware",
            ],
            1045,
        ),
    ]

    for num, title, items, x in roadmap_cols:
        add_white_card(slide, x, 280, 305, 345)

        # Number circle
        circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(x + 18), Pt(300), Pt(40), Pt(40))
        circ.fill.solid()
        circ.fill.fore_color.rgb = PILL_PINK
        circ.line.fill.background()
        tf_c = circ.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.text = str(num)
        p_c.font.size = Pt(17)
        p_c.font.bold = True
        p_c.font.color.rgb = RGBColor(0, 0, 0)
        p_c.alignment = PP_ALIGN.CENTER

        tb_t = slide.shapes.add_textbox(Pt(x + 18), Pt(355), Pt(270), Pt(45))
        p_t = tb_t.text_frame.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(18)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_TITLE

        tb_b = slide.shapes.add_textbox(Pt(x + 18), Pt(410), Pt(270), Pt(200))
        tf_b = tb_b.text_frame
        for item in items:
            p = tf_b.add_paragraph()
            p.text = item
            p.font.size = Pt(13)
            p.font.color.rgb = TEXT_BODY

    # Bottom Round 2 Goal Bar
    r2_bar = add_white_card(slide, 85, 645, 1265, 70)
    tb_r2 = slide.shapes.add_textbox(Pt(105), Pt(655), Pt(1225), Pt(50))
    p_r2 = tb_r2.text_frame.paragraphs[0]
    p_r2.text = "Round 2 goal: scan real repositories with measured accuracy, and run the period-finding circuit on real quantum hardware."
    p_r2.font.size = Pt(15)
    p_r2.font.bold = True
    p_r2.font.color.rgb = TEXT_TITLE
    p_r2.alignment = PP_ALIGN.CENTER


# ==============================================================================
# Slide 10: References & Sources
# ==============================================================================
def build_slide_10(prs):
    slide = create_blank_slide(prs)
    add_standard_header(slide, "References and Sources", "Standards, Research and Foundations")

    # Left: Standards & Research
    add_white_card(slide, 85, 275, 615, 385)
    tb_std_t = slide.shapes.add_textbox(Pt(105), Pt(290), Pt(575), Pt(35))
    p_std_t = tb_std_t.text_frame.paragraphs[0]
    p_std_t.text = "Standards & research"
    p_std_t.font.size = Pt(18)
    p_std_t.font.bold = True
    p_std_t.font.color.rgb = TEXT_TITLE

    std_items = [
        "• NIST FIPS 203 (ML-KEM), 204 (ML-DSA), 205 (SLH-DSA), Aug 2024.",
        "• NIST IR 8547 (initial public draft), Transition to Post-Quantum Cryptography, Nov 2024",
        "• P. W. Shor, Polynomial-time algorithms for prime factorization on quantum computer, 1997",
        "• L. K. Grover, A fast quantum mechanical algorithm for database search, STOC 1996",
        "• M. Mosca, Cybersecurity in an era with quantum computers: will we be ready?, IEEE 2018",
        "• C. Gidney, M. Ekerå, Factor 2048-bit RSA in 8h using 20M noisy qubits, arXiv:1905.09749",
        "• C. Gidney, Factor 2048-bit RSA with less than a million noisy qubits, arXiv:2505.15917",
    ]
    tb_std_b = slide.shapes.add_textbox(Pt(105), Pt(330), Pt(575), Pt(315))
    tf_std = tb_std_b.text_frame
    for item in std_items:
        p = tf_std.add_paragraph()
        p.text = item
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_BODY

    # Right: Software & Documentation
    add_white_card(slide, 725, 275, 625, 385)
    tb_sw_t = slide.shapes.add_textbox(Pt(745), Pt(290), Pt(585), Pt(35))
    p_sw_t = tb_sw_t.text_frame.paragraphs[0]
    p_sw_t.text = "Software & documentation"
    p_sw_t.font.size = Pt(18)
    p_sw_t.font.bold = True
    p_sw_t.font.color.rgb = TEXT_TITLE

    sw_items = [
        "• pyca/cryptography: ML-KEM, ML-DSA, AES-GCM, HKDF bindings",
        "• FastAPI, NumPy, Pydantic, Uvicorn, SQLite",
        "• Anthropic Claude & Google Gemini APIs (Security Copilot)",
        "• CycloneDX 1.6 Cryptographic Bill of Materials (CBOM) specification",
        "• Open Quantum Safe (OQS) project (architectural reference)",
    ]
    tb_sw_b = slide.shapes.add_textbox(Pt(745), Pt(330), Pt(585), Pt(180))
    tf_sw = tb_sw_b.text_frame
    for item in sw_items:
        p = tf_sw.add_paragraph()
        p.text = item
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_BODY

    # Originality Box inside right card
    orig_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(745), Pt(525), Pt(585), Pt(115))
    orig_box.fill.solid()
    orig_box.fill.fore_color.rgb = RGBColor(243, 244, 246)
    orig_box.line.color.rgb = ACCENT_CYAN
    tf_o = orig_box.text_frame
    tf_o.word_wrap = True
    p_o_t = tf_o.paragraphs[0]
    p_o_t.text = "Originality Statement"
    p_o_t.font.size = Pt(13)
    p_o_t.font.bold = True
    p_o_t.font.color.rgb = TEXT_TITLE

    p_o_b = tf_o.add_paragraph()
    p_o_b.text = "Q-SHIELD is our team's original implementation engineered for Q-Hack India 2026. Foundational libraries are consumed as dependencies, not forked or copied."
    p_o_b.font.size = Pt(11)
    p_o_b.font.color.rgb = TEXT_BODY


def main():
    prs = Presentation()
    prs.slide_width = Pt(SLIDE_WIDTH_PT)
    prs.slide_height = Pt(SLIDE_HEIGHT_PT)

    build_slide_1(prs)
    build_slide_2(prs)
    build_slide_3(prs)
    build_slide_4(prs)
    build_slide_5(prs)
    build_slide_6(prs)
    build_slide_7(prs)
    build_slide_8(prs)
    build_slide_9(prs)
    build_slide_10(prs)

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_pptx = os.path.join(root_dir, "Q-SHIELD.pptx")
    prs.save(output_pptx)
    print(f"[+] Successfully generated PowerPoint deck: {output_pptx}")

    # Export PDF via LibreOffice
    import subprocess
    cmd = ["libreoffice", "--headless", "--convert-to", "pdf", output_pptx, "--outdir", root_dir]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Rename Q-SHIELD.pdf to Q-SHIELD.pptx.pdf
        gen_pdf = os.path.join(root_dir, "Q-SHIELD.pdf")
        target_pdf = os.path.join(root_dir, "Q-SHIELD.pptx.pdf")
        if os.path.exists(gen_pdf):
            if os.path.exists(target_pdf):
                os.remove(target_pdf)
            os.rename(gen_pdf, target_pdf)
            print(f"[+] Successfully updated PDF presentation: {target_pdf}")
    except Exception as e:
        print(f"[!] Warning: Could not auto-convert to PDF via LibreOffice: {e}")


if __name__ == "__main__":
    main()
