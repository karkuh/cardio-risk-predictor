import streamlit.components.v1 as components
import json
import random

def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def show_full_screen_animation(lottie_json, direction="left-to-right", centered=False):
    if lottie_json is None:
        return

    unique_id = f"lottie-overlay-{random.randint(0, 999999)}"
    json_str = json.dumps(lottie_json)

    if centered:
        start_pos = "50vw"
        end_translate = None
    else:
        if direction == "left-to-right":
            start_pos = "-10vw"
            end_translate = "200vw"
        else:
            start_pos = "110vw"
            end_translate = "-180vw"

    html_code = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.10.1/lottie.min.js"></script>
    <script>
        const parentDoc = window.parent.document;
        parentDoc.querySelectorAll("[id^='lottie-overlay-']").forEach(el => el.remove());

        const overlay = parentDoc.createElement("div");
        overlay.id = "{unique_id}";
        overlay.style.position = "fixed";
        overlay.style.top = "0";
        overlay.style.left = "0";
        overlay.style.width = "100vw";
        overlay.style.height = "100vh";
        overlay.style.zIndex = "999999999";
        overlay.style.pointerEvents = "none";
        overlay.style.background = "transparent";
        overlay.style.overflow = "visible";
        parentDoc.body.appendChild(overlay);

        const animData = {json_str};
        const wrapper = parentDoc.createElement("div");
        wrapper.style.position = "absolute";
        wrapper.style.top = "50%";
        wrapper.style.left = "{start_pos}";
        wrapper.style.transform = "translate(-50%, -50%)";
        wrapper.style.width = "100vmin";
        wrapper.style.height = "100vmin";
        overlay.appendChild(wrapper);

        const anim = lottie.loadAnimation({{
            container: wrapper,
            renderer: "svg",
            loop: false,
            autoplay: true,
            animationData: animData
        }});

        anim.setSpeed(2.0);

        {f'''
        wrapper.animate([
            {{ transform: "translate(-50%, -50%) translateX(0vw)" }},
            {{ transform: "translate(-50%, -50%) translateX({end_translate})" }}
        ], {{
            duration: anim.getDuration() * 500,
            easing: "linear",
            fill: "forwards"
        }});
        ''' if not centered else ''}

        anim.addEventListener("complete", () => {{
            overlay.remove();
        }});
    </script>
    """

    components.html(html_code, height=0, width=0)
