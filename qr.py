import streamlit as st
from osmnx.geocoder import geocode
from segno import helpers
import segno
import io
from PIL import Image
import uuid

st.write("""
# Generate QR Codes
No Data is saved on the server, all data is processed on the client side or in memory on the server (e.g. Logo).
""")

tab1, tab2, tab3, tab4 = st.tabs(["Address", "Lat long", "Link", "Link & Logo"])

@st.cache_data(experimental_allow_widgets=True)
def show_qr(_img, _buff):
    st.download_button("Download QR Code", _buff, f"qr_code.png", "image/png", use_container_width=True,
                       key=uuid.uuid4(),
                       type="primary")
    st.image(_img, caption="QR Code, you can test it by using your mobile phone", use_column_width=True, )


def generate_geo_qr(lat, lon, scale=30, border=1, light='#FFFFFF', dark='#000000', **kwargs_img) -> Image:
    qr_code = helpers.make_geo(float(lat), float(lon), )
    buff = io.BytesIO()
    qr_code.save(buff, kind='png', scale=scale, border=border, light=light, dark=dark, **kwargs_img)
    buff.seek(0)  # Important to let PIL / Pillow load the image
    img = Image.open(buff)
    return buff, img


def generate_qr(url, error, version, mode, scale=30, border=1, light='#FFFFFF', dark='#000000', **kwargs_img) -> Image:
    qr_code = segno.make_qr(url, error=error, version=version, mode=mode)
    buff = io.BytesIO()
    qr_code.save(buff, kind='png', scale=scale, border=border, light=light, dark=dark, **kwargs_img)
    buff.seek(0)  # Important to let PIL / Pillow load the image
    img = Image.open(buff)
    return buff, img


def generate_qr_with_img(url, logo, size, version, mode, scale=30, border=1, light='#FFFFFF', dark='#000000',
                         **kwargs_img) -> Image:
    qr_code = segno.make_qr(url, error='h', version=version, mode=mode)

    buff = io.BytesIO()
    qr_code.save(buff, kind='png', scale=scale, border=border, light=light, dark=dark, **kwargs_img)
    buff.seek(0)  # Important to let PIL / Pillow load the image
    img = Image.open(buff).convert("RGBA")

    ing_width, img_height = img.size
    logo_max_size = img_height * size/100

    logo_img = Image.open(logo).convert("RGBA")

    logo_img.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)

    box = ((ing_width - logo_img.size[0]) // 2, (img_height - logo_img.size[1]) // 2)
    img.paste(logo_img, box, logo_img)
    img.save(buff, "PNG")

    return buff, img


with tab1:
    with st.form(key='my_form'):
        address = st.text_input("Location address", help="Enter the address you want to create a qr code for")
        col1, col2 = st.columns(2)
        with col1:
            bg_color = st.color_picker('Background Color', value='#FFFFFF',
                                       help="Background color of the qr code in hex format or name")
            scale = st.slider('Scale of picture', min_value=1, max_value=50, value=30,
                              help="Higher values result in a higher resolution image")
        with col2:
            fg_color = st.color_picker('QR Color', value='#000000',
                                       help="Color of the qr code itself in hex format or name")
            border = st.slider('Border', min_value=0, max_value=10, value=1,
                               help="Higher values result in a larger border")

        expander1 = st.expander("Advanced Color Options:")
        dark = fg_color
        light = bg_color
        alignment_dark = expander1.color_picker('alignment_dark', value=dark)
        alignment_light = expander1.color_picker('alignment_light', value=light)
        dark_module = expander1.color_picker('dark_module', value=dark)
        data_dark = expander1.color_picker('data_dark', value=dark)
        data_light = expander1.color_picker('data_light', value=light)
        finder_dark = expander1.color_picker('finder_dark', value=dark)
        finder_light = expander1.color_picker('finder_light', value=light)
        format_dark = expander1.color_picker('format_dark', value=dark)
        format_light = expander1.color_picker('format_light', value=light)
        quiet_zone = expander1.color_picker('quiet_zone', value=light)
        params_img = {"alignment_dark": alignment_dark, "alignment_light": alignment_light,
                      "dark_module": dark_module, "data_dark": data_dark, "data_light": data_light,
                      "finder_dark": finder_dark, "finder_light": finder_light, "format_dark": format_dark,
                      "format_light": format_light, "quiet_zone": quiet_zone}

        st.form_submit_button('Generate QR Code', use_container_width=True)

        placeholder = st.empty()
    try:
        if address != "":
            show_qr.clear()
            lat, lon = geocode(address)
            st.write(f"Created qr code for {address} at {lat}, {lon}")
            buff, img = generate_geo_qr(lat, lon, scale=scale, border=border, light=bg_color, dark=fg_color,
                                        **params_img)
            show_qr(img, buff)

    except ValueError as e:
        st.error(str(e))
        st.stop()

with tab2:
    with st.form(key='my_form2'):
        col3, col4 = st.columns(2)

        with col3:
            lat = st.text_input("Latitude", )
            bg_color = st.color_picker('Background Color', value='#FFFFFF',
                                       help="Background color of the qr code in hex format or name")
            scale = st.slider('Scale of picture', min_value=1, max_value=50, value=30,
                              help="Higher values result in a higher resolution image")
        with col4:
            long = st.text_input("Longitude", )
            fg_color = st.color_picker('QR Color', value='#000000',
                                       help="Color of the qr code itself in hex format or name")
            border = st.slider('Border', min_value=0, max_value=10, value=1,
                               help="Higher values result in a larger border")

        expander2 = st.expander("Advanced Color Options:")
        dark = fg_color
        light = bg_color
        alignment_dark = expander2.color_picker('alignment_dark', value=dark)
        alignment_light = expander2.color_picker('alignment_light', value=light)
        dark_module = expander2.color_picker('dark_module', value=dark)
        data_dark = expander2.color_picker('data_dark', value=dark)
        data_light = expander2.color_picker('data_light', value=light)
        finder_dark = expander2.color_picker('finder_dark', value=dark)
        finder_light = expander2.color_picker('finder_light', value=light)
        format_dark = expander2.color_picker('format_dark', value=dark)
        format_light = expander2.color_picker('format_light', value=light)
        quiet_zone = expander2.color_picker('quiet_zone', value=light)
        params_img = {"alignment_dark": alignment_dark, "alignment_light": alignment_light,
                      "dark_module": dark_module, "data_dark": data_dark, "data_light": data_light,
                      "finder_dark": finder_dark, "finder_light": finder_light, "format_dark": format_dark,
                      "format_light": format_light, "quiet_zone": quiet_zone}

        st.form_submit_button('Generate QR Code', use_container_width=True)

    try:
        if lat != "" and long != "":
            show_qr.clear()
            st.write(f"Created qr code for {lat}, {long}")
            buff, img = generate_geo_qr(lat, long, scale=scale, border=border, light=bg_color, dark=fg_color,
                                        **params_img
                                        )
            show_qr(img, buff)

    except ValueError as e:
        st.error(str(e))
        st.stop()

with (tab3):
    with st.form(key='my_form3'):
        link = st.text_input("Link")
        col5, col6 = st.columns(2)

        with col5:
            bg_color = st.color_picker('Background Color', value='#FFFFFF',
                                       help="Background color of the qr code in hex format or name")
            scale = st.slider('Scale of picture', min_value=1, max_value=50, value=30,
                              help="Higher values result in a higher resolution image")
        with col6:
            fg_color = st.color_picker('QR Color', value='#000000',
                                       help="Color of the qr code itself in hex format or name")
            border = st.slider('Border', min_value=0, max_value=10, value=1,
                               help="Higher values result in a larger border")

        expander = st.expander("Advanced Options:")
        expander.write("Don't change these unless you know what you're doing")
        error = expander.selectbox("Error", [None, "L", "M", "Q", "H", "-"], index=2)
        version = expander.selectbox("Version", [None, *range(1, 41)], index=0)
        mode = expander.selectbox("Mode", [None, "alphanumeric", "byte", "numeric", "kanji", "hanzi"], index=0)

        expander2 = st.expander("Advanced Color Options:")
        dark = fg_color
        light = bg_color
        alignment_dark = expander2.color_picker('alignment_dark', value=dark)
        alignment_light = expander2.color_picker('alignment_light', value=light)
        dark_module = expander2.color_picker('dark_module', value=dark)
        data_dark = expander2.color_picker('data_dark', value=dark)
        data_light = expander2.color_picker('data_light', value=light)
        finder_dark = expander2.color_picker('finder_dark', value=dark)
        finder_light = expander2.color_picker('finder_light', value=light)
        format_dark = expander2.color_picker('format_dark', value=dark)
        format_light = expander2.color_picker('format_light', value=light)
        quiet_zone = expander2.color_picker('quiet_zone', value=light)
        params_img = {"alignment_dark": alignment_dark, "alignment_light": alignment_light,
                      "dark_module": dark_module, "data_dark": data_dark, "data_light": data_light,
                      "finder_dark": finder_dark, "finder_light": finder_light, "format_dark": format_dark,
                      "format_light": format_light, "quiet_zone": quiet_zone}

        st.form_submit_button('Generate QR Code', use_container_width=True)

    try:
        if link != "":
            show_qr.clear()
            st.write(f"Created qr code for {link}")
            buff, img = generate_qr(link, scale=scale, border=border, light=bg_color, dark=fg_color,
                                    error=error, version=version, mode=mode,
                                    **params_img
                                    )
            show_qr(img, buff)

    except ValueError as e:
        st.error(str(e))
        st.stop()

with (tab4):
    with st.form(key='my_form4'):
        link = st.text_input("Link")

        uploaded_logo = st.file_uploader("Upload Logo", accept_multiple_files=False, type=["png", "jpg", "jpeg"],
                                         help="Upload a logo to be placed in the center of the qr code",
                                         )

        col7, col8 = st.columns(2)

        with col7:
            bg_color = st.color_picker('Background Color', value='#FFFFFF',
                                       help="Background color of the qr code in hex format or name")
            scale = st.slider('Scale of picture', min_value=1, max_value=50, value=30,
                              help="Higher values result in a higher resolution image")
        with col8:
            fg_color = st.color_picker('QR Color', value='#000000',
                                       help="Color of the qr code itself in hex format or name")
            border = st.slider('Border', min_value=0, max_value=10, value=1,
                               help="Higher values result in a larger border")

        expander = st.expander("Advanced Options:")
        expander.write("Don't change these unless you know what you're doing")
        # error = expander.selectbox("Error", [None, "L", "M", "Q", "H", "-"], index=2)
        version = expander.selectbox("Version", [None, *range(1, 41)], index=0)
        mode = expander.selectbox("Mode", [None, "alphanumeric", "byte", "numeric", "kanji", "hanzi"], index=0)
        expander.write("Be aware that adding a logo will negatively influence the readability of the QR Code. "
                 "Thus the logo should not be too big. Always test it!")
        size = expander.slider("Size in %", min_value=1, max_value=100, value=33, help="Size of the logo in % of the qr code")

        expander2 = st.expander("Advanced Color Options:")
        dark = fg_color
        light = bg_color
        alignment_dark = expander2.color_picker('alignment_dark', value=dark)
        alignment_light = expander2.color_picker('alignment_light', value=light)
        dark_module = expander2.color_picker('dark_module', value=dark)
        data_dark = expander2.color_picker('data_dark', value=dark)
        data_light = expander2.color_picker('data_light', value=light)
        finder_dark = expander2.color_picker('finder_dark', value=dark)
        finder_light = expander2.color_picker('finder_light', value=light)
        format_dark = expander2.color_picker('format_dark', value=dark)
        format_light = expander2.color_picker('format_light', value=light)
        quiet_zone = expander2.color_picker('quiet_zone', value=light)
        params_img = {"alignment_dark": alignment_dark, "alignment_light": alignment_light,
                      "dark_module": dark_module, "data_dark": data_dark, "data_light": data_light,
                      "finder_dark": finder_dark, "finder_light": finder_light, "format_dark": format_dark,
                      "format_light": format_light, "quiet_zone": quiet_zone}

        st.form_submit_button('Generate QR Code', use_container_width=True)

    try:
        if link != "" and uploaded_logo is not None:
            show_qr.clear()
            st.write(f"Created qr code for {link}")
            buff, img = generate_qr_with_img(link, logo=uploaded_logo, scale=scale, border=border, light=bg_color,
                                             dark=fg_color, size=size,
                                             version=version, mode=mode, **params_img
                                             )
            show_qr(img, buff)

    except ValueError as e:
        st.error(str(e))
        st.stop()


