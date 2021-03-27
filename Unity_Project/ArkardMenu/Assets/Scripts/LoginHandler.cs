using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Drawing;

public class LoginHandler : MonoBehaviour
{
    public TextMeshProUGUI userDisplay;
    public TextMeshProUGUI passDisplay;

    public TMP_InputField user_InputField;
    public TMP_InputField pass_InputField;

    public TextMeshProUGUI brokerDisplay;
    public TextMeshProUGUI portDisplay;

    public TMP_InputField broker_InputField;
    public TMP_InputField port_InputField;

    public string s_user;
    public string s_pass;
    public string s_broker;
    public string s_port;

    public Image myImage;
    public Sprite Sprite1;
    public Sprite Sprite2;
    public Sprite Sprite3;
    //TODO add in MRTK keyboard

    public void setText()
    {

        s_user = user_InputField.text;
        s_pass = pass_InputField.text;
        s_broker = broker_InputField.text;
        s_port = port_InputField.text;
        //s_user and s_pass passed to MQTT to send to MySql 

        userDisplay.text = s_user;
        passDisplay.text = s_pass;
        brokerDisplay.text = s_broker;
        portDisplay.text = s_port;

        //TODO: append DenyOrAllow here
    }
    public void reset() //Used to manually disconnect
    {
        userDisplay.text = "RESET";
        passDisplay.text = "RESET";
        brokerDisplay.text = "RESET";
        portDisplay.text = "RESET";
        myImage.sprite = Sprite3;

    }
    public void DenyOrAllow() //TODO: Add this for successful MySQl Login
    {
        int i = 0;
        if (myImage.enabled == false)
        {
            myImage.enabled = true;
        }
        else
        {
            if (i==1)
            {
                myImage.sprite = Sprite1;
            }
            else {
                myImage.sprite = Sprite2;
            }
        }
    }
}
