class OTP_email():
    def OTP(otp):

        html = """\
            <head>
                    <meta name="viewport" content="width=device-width">
                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                    <title>Civil Academy Email Template</title>
                    <style media="all" type="text/css">
                    @media only screen and (max-width: 480px) {{
                        table[class=body] h1 {{
                            font-size: 24px !important;
                        }}
                        table[class=body] h2 {{
                            font-size: 20px !important;
                        }}
                        table[class=body] h3 {{
                            font-size: 14px !important;
                        }}
                        table[class=body] .content,
                        table[class=body] .wrapper {{
                            padding: 15px !important;
                        }}
                        table[class=body] .container {{
                            width: 100% !important;
                            padding: 0 !important;
                        }}
                        table[class=body] .column {{
                            width: 100% !important;
                        }}
                        table[class=body] .stats .column {{
                            width: 50% !important;
                        }}
                        table[class=body] .hero-image,
                        table[class=body] .thumb {{
                            width: 100% !important;
                            height: auto !important;
                        }}
                        table[class=body] .btn table,
                        table[class=body] .btn a {{
                            width: 100% !important;
                        }}
                        table[class=body] .stats-table {{
                            display: none !important;
                        }}
                        table[class=body] .stats-labels .label,
                        table[class=body] .category-labels .label {{
                            font-size: 10px !important;
                        }}
                        table[class=body] .credits table {{
                            table-layout: auto !important;
                        }}
                        table[class=body] .credits .label {{
                            font-size: 11px !important;
                        }}
                    }}
                    </style>
                    <style type="text/css">
                    @font-face {{
                        font-family: 'Open Sans';
                        font-style: normal;
                        font-weight: 300;
                        src: local('Open Sans Light'), local('OpenSans-Light'), url(https://fonts.gstatic.com/s/opensans/v13/DXI1ORHCpsQm3Vp6mXoaTYnF5uFdDttMLvmWuJdhhgs.ttf) format('truetype');
                    }}
                    
                    @font-face {{
                        font-family: 'Open Sans';
                        font-style: normal;
                        font-weight: 400;
                        src: local('Open Sans'), local('OpenSans'), url(https://fonts.gstatic.com/s/opensans/v13/cJZKeOuBrn4kERxqtaUH3aCWcynf_cDxXwCLxiixG1c.ttf) format('truetype');
                    }}
                    
                    @font-face {{
                        font-family: 'Open Sans';
                        font-style: normal;
                        font-weight: 600;
                        src: local('Open Sans Semibold'), local('OpenSans-Semibold'), url(https://fonts.gstatic.com/s/opensans/v13/MTP_ySUJH_bn48VBG8sNSonF5uFdDttMLvmWuJdhhgs.ttf) format('truetype');
                    }}
                    </style>
                </head>

                <body style="font-size: 16px; background-color: #fdfdfd; margin: 0; padding: 0; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; -webkit-text-size-adjust: 100%; line-height: 1.5; -ms-text-size-adjust: 100%; -webkit-font-smoothing: antialiased; height: 100% !important; width: 100% !important;">
                    <table bgcolor="#fdfdfd" class="body" style="box-sizing: border-box; border-spacing: 0; mso-table-rspace: 0pt; mso-table-lspace: 0pt; width: 100%; background-color: #fdfdfd; border-collapse: separate !important;" width="100%">
                        <tbody>
                            <tr>
                                <td style="box-sizing: border-box; padding: 0; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 16px; vertical-align: top;" valign="top">&nbsp;</td>
                                <td class="container" style="box-sizing: border-box; padding: 0; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 16px; vertical-align: top; display: block; width: 600px; max-width: 600px; margin: 0 auto !important;" valign="top" width="600">
                                    <div class="content" style="box-sizing: border-box; display: block; max-width: 600px; margin: 0 auto; padding: 10px;"><span class="preheader" style="color: transparent; display: none; height: 0; max-height: 0; max-width: 0; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden; width: 0;">Let's confirm your email address.</span>
                                        <div class="header" style="box-sizing: border-box; width: 100%; margin-bottom: 30px; margin-top: 15px;">
                                            <table style="box-sizing: border-box; width: 100%; border-spacing: 0; mso-table-rspace: 0pt; mso-table-lspace: 0pt; border-collapse: separate !important;" width="100%">
                                                <tbody>
                                                    <tr>
                                                        <td align="left" class="align-left" style="box-sizing: border-box; padding: 0; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 16px; vertical-align: top; text-align: left;" valign="top"><span class="sg-image" data-imagelibrary=""><a href="#" style="box-sizing: border-box; color: #348eda; font-weight: 400; text-decoration: none;" target="_blank"><img alt="Civil Academy" height="22" src="" style="max-width: 100%; border-style: none; width: 68px; height: auto;" width="68px"></a></span></td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                        <div class="block" style="box-sizing: border-box; width: 100%; margin-bottom: 30px; background: #ffffff; border: 1px solid #f0f0f0;">
                                            <table style="box-sizing: border-box; width: 100%; border-spacing: 0; mso-table-rspace: 0pt; mso-table-lspace: 0pt; border-collapse: separate !important;" width="100%">
                                                <tbody>
                                                    <tr>
                                                        <td class="wrapper" style="box-sizing: border-box; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 16px; vertical-align: top; padding: 30px;" valign="top">
                                                            <table style="box-sizing: border-box; width: 100%; border-spacing: 0; mso-table-rspace: 0pt; mso-table-lspace: 0pt; border-collapse: separate !important;" width="100%">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="box-sizing: border-box; padding: 0; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 16px; vertical-align: top;" valign="top">
                                                                            <h2 style="margin: 0; margin-bottom: 30px; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-weight: 300; line-height: 1.5; font-size: 24px; color: #294661 !important;">You're on your way!<br>
                                                    Let's confirm your email address.</h2>
                                                                            <p style="margin: 0; margin-bottom: 30px; color: #294661; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 300;">Use below mentioned code to confirm your email address </p>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td style="box-sizing: border-box; padding: 0; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 16px; vertical-align: top;" valign="top">
                                                                            <table cellpadding="0" cellspacing="0" class="btn btn-primary" style="box-sizing: border-box; border-spacing: 0; mso-table-rspace: 0pt; mso-table-lspace: 0pt; width: 100%; border-collapse: separate !important;" width="100%">
                                                                                <tbody>
                                                                                    <tr>
                                                                                        <td align="center" style="box-sizing: border-box; padding: 0; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 16px; vertical-align: top; padding-bottom: 15px;" valign="top">
                                                                                            <table cellpadding="0" cellspacing="0" style="box-sizing: border-box; border-spacing: 0; mso-table-rspace: 0pt; mso-table-lspace: 0pt; width: auto; border-collapse: separate !important;">
                                                                                                <tbody>
                                                                                                    <tr>
                                                                                                        <td align="center" bgcolor="#348eda" style="box-sizing: border-box; padding: 0; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 16px; vertical-align: top; background-color: #348eda; border-radius: 2px; text-align: center;" valign="top"><span style="box-sizing: border-box; border-color: #348eda; font-weight: 400; text-decoration: none; display: inline-block; margin: 0; color: #ffffff;background: rgb(47,58,147);
                background: radial-gradient(circle, rgba(47,58,147,1) 55%, rgba(244,141,48,1) 55%); border-radius: 2px; cursor: copy; font-size: 14px; padding: 6px 25px;" target="_blank">{}</span></td>
                                                                                                    </tr>
                                                                                                </tbody>
                                                                                            </table>
                                                                                        </td>
                                                                                    </tr>
                                                                                </tbody>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                        <div class="footer" style="box-sizing: border-box; clear: both; width: 100%;">
                                            <table style="box-sizing: border-box; width: 100%; border-spacing: 0; mso-table-rspace: 0pt; mso-table-lspace: 0pt; font-size: 12px; border-collapse: separate !important;" width="100%">
                                                <tbody>
                                                    <tr style="font-size: 12px;">
                                                        <td align="center" class="align-center" style="box-sizing: border-box; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; vertical-align: top; font-size: 12px; text-align: center; padding: 20px 0;" valign="top"><span class="sg-image" style="float: none; display: block; text-align: center;"><a href="https://sendgrid.com?utm_campaign=website&amp;utm_source=sendgrid.com&amp;utm_medium=email" style="box-sizing: border-box; color: #348eda; font-weight: 400; text-decoration: none; font-size: 12px;" target="_blank"><img alt="Civil Academy" height="16" src="https://i.ibb.co/R2B4jYx/civil.png" style="max-width: 100%; border-style: none; font-size: 12px; width: 48px; height: 48px;" width="89"></a></span>
                                                            <p class="tagline" style="color: #294661; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-size: 12px; font-weight: 400; margin-bottom: 5px; margin: 10px 0 20px;">Send with Confidence</p>
                                                            <p style="margin: 0; color: #294661; font-family: 'Open Sans', 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif; font-weight: 300; font-size: 12px; margin-bottom: 5px;">© Civil Academy. Umm Ramool-Behind Dubai Duty Free Wherhouse</p>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                </body>
            </html>
        """.format(otp)

        return html




class OTP_email1():
    def OTP(otp):
        html = """\
            <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
            <div style="margin:50px auto;width:70%;padding:20px 0">
                <div style="border-bottom:1px solid #eee">
                <img src="logo-main-black.png" />
                </div>
                <p style="font-size:1.1em">Hi,</p>
                <p>Thank you for choosing Your Brand. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
                <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">324457</h2>
                <p style="font-size:0.9em;">Regards,<br />Your Brand</p>
                <hr style="border:none;border-top:1px solid #eee" />
                <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
                <p>Your Brand Inc</p>
                <p>1600 Amphitheatre Parkway</p>
                <p>California</p>
                </div>
            </div>
            </div>
            """

        return html

# <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Your Brand</a>