using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Drawing;

public class LoginHandler : MonoBehaviour
{

    public TMP_InputField user_InputField;
    public TextMeshProUGUI user_out;

    public TMP_InputField pass_InputField;
    public TextMeshProUGUI pass_out;

    public TMP_InputField broker_InputField;
    public TextMeshProUGUI broker_out;

    public TMP_InputField port_InputField;
    public TextMeshProUGUI port_out;

    public TextMeshProUGUI MQTTMsgDisplay; // G:0, 255, 205, 255 R:255, 0, 0, 255 Y:236, 190, 2, 255
    public Button ConnectButton;
    public Button SetUpButton;
    public Button DisconnectButton;

    public GameObject Logo; //RectTransform, Image.sprite
    public Sprite ConnectionSprite;
    public Sprite FailureSprite;
    public Sprite SetupSprite;
    public Sprite CompleteSprite;
    
    public string s_user;
    public string s_pass;
    public string s_broker;
    public string s_port;

    public bool loginSuccess;
    //TODO add in MRTK keyboard???
    public void Start()
    {
        //ConnectButton.onClick.AddListener(() => LoginConnect());
    }

    public void LoginConnect()
    {

        s_user = user_InputField.text;
        s_pass = pass_InputField.text;
        s_broker = broker_InputField.text;
        s_port = port_InputField.text;
        //strings to be passed to MQTT to send to Connect() in mqttManager_ARK.c
        user_out.text += s_user;
        pass_out.text += s_pass;
        broker_out.text += s_broker;
        port_out.text += s_port;

        user_out.gameObject.GetComponent<RectTransform>().anchoredPosition = new Vector3(205, -20, 0);
        pass_out.gameObject.GetComponent<RectTransform>().anchoredPosition = new Vector3(205, -50, 0);
        broker_out.gameObject.GetComponent<RectTransform>().anchoredPosition = new Vector3(205, -80, 0);
        port_out.gameObject.GetComponent<RectTransform>().anchoredPosition = new Vector3(205, -110, 0);

        user_InputField.gameObject.SetActive(false);
        pass_InputField.gameObject.SetActive(false);
        broker_InputField.gameObject.SetActive(false);
        port_InputField.gameObject.SetActive(false);

        Logo.GetComponent<RectTransform>().anchoredPosition = new Vector3(170, -240, 0);
        Logo.GetComponent<RectTransform>().localScale = new Vector3((float)1.5, (float)1.5, (float)1.5);

        ConnectButton.gameObject.SetActive(false);

        //Display connect message and resize logo
        MQTTMsgDisplay.fontSize = 18;
        MQTTMsgDisplay.gameObject.SetActive(true);
        if (!loginSuccess)
        {
            Logo.GetComponent<Image>().sprite = FailureSprite;
            MQTTMsgDisplay.color = new Color32(255, 0, 0, 255);
            MQTTMsgDisplay.text = "Connection Failed..."; //receives mqtt status message
            DisconnectButton.gameObject.SetActive(true);
        }
        else 
        {
            Logo.GetComponent<Image>().sprite = SetupSprite;
            MQTTMsgDisplay.color = new Color32(236, 190, 2, 255);
            MQTTMsgDisplay.text = "Connected...\n" + "Please setup your anchors"; //receives mqtt status message        
            SetUpButton.gameObject.SetActive(true);
        }
    }

    public void LoginSetup()
    {
        Logo.GetComponent<Image>().sprite = CompleteSprite;
        MQTTMsgDisplay.fontSize = 30;
        MQTTMsgDisplay.color = new Color32(0, 255, 205, 255);
        MQTTMsgDisplay.text = "ARKARDS";
        SetUpButton.gameObject.SetActive(false);
        DisconnectButton.gameObject.SetActive(true);
    }

    public void LoginDisconnect()
    {
        user_out.text = "Username: ";
        pass_out.text = "Password: ";
        broker_out.text = "Broker: ";
        port_out.text = "Port: ";

        user_out.gameObject.GetComponent<RectTransform>().anchoredPosition = new Vector3(205, -110, 0);
        pass_out.gameObject.GetComponent<RectTransform>().anchoredPosition = new Vector3(205, -178, 0);
        broker_out.gameObject.GetComponent<RectTransform>().anchoredPosition = new Vector3(205, -245, 0);
        port_out.gameObject.GetComponent<RectTransform>().anchoredPosition = new Vector3(205, -320, 0);

        user_InputField.gameObject.SetActive(true);
        pass_InputField.gameObject.SetActive(true);
        broker_InputField.gameObject.SetActive(true);
        port_InputField.gameObject.SetActive(true);

        Logo.GetComponent<RectTransform>().anchoredPosition = new Vector3(170, -52, 0);
        Logo.GetComponent<RectTransform>().localScale = new Vector3((float)0.9, (float)0.9, (float)0.9);
        Logo.GetComponent<Image>().sprite = ConnectionSprite;

        MQTTMsgDisplay.gameObject.SetActive(false);
        DisconnectButton.gameObject.SetActive(false);
        ConnectButton.gameObject.SetActive(true);
    }
}
