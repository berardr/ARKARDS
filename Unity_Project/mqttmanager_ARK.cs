using Newtonsoft.Json;
using System;
using System.Net.Sockets;
using TMPro;
using UnityEngine;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;

public class mqttmanager_ARK : MonoBehaviour
{
    #region Properties
    /// <summary>
    /// Mqtt properties
    /// </summary>
    private MqttClient client;
    private string broker;
    private int port;
    private bool secure;
    private MqttSslProtocols sslprotocol;
    private MqttProtocolVersion protocolversion;
    private string username;
    private string password;
    private string clientId;
    private string topic;
    private bool publish = false;
    private byte qos;
    private bool retain;
    private bool cleansession;
    private ushort keepalive;

    /// <summary>
    /// Data properties
    /// </summary>
    private bool dataHasBeenUpdated;

    /// <summary>
    /// Text objects assoicated with the Mqtt data
    /// </summary>

    /// <summary>
    /// Menu UI
    /// </summary>
    public  LoginHandler login;
    #endregion

    #region Initilization
    /// <summary>
    /// Start is called before the first frame update.
    /// </summary>
    public class LoginMsg
    {
        public string MySQLUser { get; set; }
        public string MySQLPass { get; set; }


    }
    public class LoginResponse
    {
        public int Success { get; set; }
        public string ErrorMsg { get; set; }
    }
    private void Start()
    {
        //Set up default Mqtt properties for https://github.com/khilscher/MqttClient
        broker = "mqtt.eclipse.org";
        port = 1883;
        secure = false;
        sslprotocol = MqttSslProtocols.None;
        protocolversion = MqttProtocolVersion.Version_3_1_1;
        username = "";
        password = "";
        clientId = username;
        publish = false;
        qos = (byte)2;
        retain = false;
        cleansession = false;
        keepalive = 60;
        topic_login = "ARK/Login";
        topic_tag = "ARK/Tag";
        topic_anchor = "ARK/Anchor";

        //Update the settings menu with default values
        //login.user_InputField.text = username
        //login.pass_InputField.text = password
        login.broker_InputField.text = broker;
        login.port_InputField.text = port;


        //Default data properties
        
        dataHasBeenUpdated = false;
        loginResponse = false;
        anchorResponse = false;


        //Add callback methods for setting ui
        login.EnterButton.OnClick.AddListener(() => Connect());
    }
    #endregion

    #region Methods

    /// <summary>
    /// Connect to MySQL and MQTT when Enter button is pushed
    /// </summary>
    public void Connect()
    {
        //Connect to MQTT
        MqttConnect()
        //Publsih message to connect to MySQL
        LoginMsg loginmsg = new LoginMsg();
        loginmsg.MySQLPass = this.password
        loginmsg.MySQLUser = this.username
        LoginResponse loginresponse = new LoginResponse();
        string login_msg = JsonConver.SerializeObject(loginmsg)
        MqttPublish(this.topic_login, login_msg)
        MqttSubscribe(this.topic_login)

        

    }
    /// <summary>
    /// Update is called every frame, if the MonoBehaviour is enabled.
    /// </summary>
    private void Update()
    {
        //if we have new data, update the corresponding text in the scene
        if (dataHasBeenUpdated)
        {
            //Message Recieved: update data
            dataHasBeenUpdated = false;
        }
    }

    /// <summary>
    /// Updated MQTT based on values in the setting menu.
    /// </summary>
    public void UpdateMqttBasedOnSettingMenu()
    {
        username = login.user_InputField.text 
        password = login.pass_InputField.text
        //broker = login.broker_InputField.text
        //port = login.port_InputField.text
    }

    /// <summary>
    /// Connected to Mqtt.
    /// </summary>
    public void MqttConnect()
    {
        try
        {
            UpdateMqttBasedOnSettingMenu();
            client = new MqttClient(this.broker);

            // Set MQTT version
            client.ProtocolVersion = this.protocolversion;

            // Setup callback for receiving messages
            client.MqttMsgPublishReceived += ClientRecieveMessage;

            // MQTT return codes 
            // https://www.hivemq.com/blog/mqtt-essentials-part-3-client-broker-connection-establishment/
            // https://www.eclipse.org/paho/clients/dotnet/api/html/4158a883-de72-1ec4-2209-632a86aebd74.htm
            byte resp = client.Connect(this.clientId) //, this.username, this.password, this.cleansession, this.keepalive);
            settings.DebugConsole.text = "Connect() Response: " + resp.ToString();
        }
        catch (SocketException e)
        {
            //print error message to menu canvas
            settings.DebugConsole.text = e.Message;
        }
        catch (Exception e)
        {
            //print error message to menu canvas
            settings.DebugConsole.text = e.Message;

        }
    }

    /// <summary>
    /// Subscribe to predefined Mqtt topic.
    /// </summary>
    public void MqttSubscribe(topic)
    {
        if (client != null && client.IsConnected)
        {
            ushort resp = client.Subscribe(
                new string[] { topic },
                new byte[] { this.qos });

            settings.DebugConsole.text = "Subscribe() Response: " + resp.ToString();

        }
        else
        {
            settings.DebugConsole.text = "Not subscribe";

        }
    }

    /// <summary>
    /// Call back Method for recieving messages from MQTT.
    /// </summary>
    public void ClientRecieveMessage(object sender, MqttMsgPublishEventArgs e)
    {
        topic = System.Text.UTF8Encoding.UTF8.GetString(e.Topic);
        if(topic == "ARK/Login")
        {
            LoginResponse deserializedResponse = JsonConvert.DeserializeObject<LoginResponse>(System.Text.UTF8Encoding.UTF8.GetString(e.Message));
            this.loginResponse = true;
            //tag callback
        }
        else if(topic == "ARK/Anchor")
        {
            //anchor callback
        }
        else if(topic == "ARK/Tag")
        {
            //login callback
        }
        else
        {
            //unkown topic error
        }

        dataHasBeenUpdated = true;
    }

    /// <summary>
    /// Disconnect from Mqtt broker.
    /// </summary>
    private void MqttDisconnect()
    {
        if (client != null && client.IsConnected)
        {
            client.Disconnect();
            settings.DebugConsole.text = "Disconnect()";
        }
        else
        {
            settings.DebugConsole.text = "Not connected";
        }
    }

    /// <summary>
    /// Unsubscribe from Mqtt topic.
    /// </summary>
    public void MqttUnsubscribe()
    {
        if (client != null && client.IsConnected)
        {
            ushort resp = client.Unsubscribe(
                new string[] { this.topic });

            settings.DebugConsole.text = "Unsubscribe() Response: " + resp.ToString();
        }
        else
        {
            settings.DebugConsole.text = "Not connected";

        }
    }
    #endregion

    public void MqttPublish(topic, msg)
    {
        
        client.Publish(topic, System.Text.Encoding.UTF8.GetBytes(msg), this.qos, this.retain);
        Debug.Log("Login message published");
    }
}

