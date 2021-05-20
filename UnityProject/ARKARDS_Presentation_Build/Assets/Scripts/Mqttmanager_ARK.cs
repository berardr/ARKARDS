using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Linq;
using System.Net.Sockets;
using TMPro;
using UnityEngine;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using MathNet.Numerics.LinearAlgebra;
using MathNet.Numerics.LinearAlgebra.Double;



public class Mqttmanager_ARK : MonoBehaviour
{
    #region Properties
    /// <summary>
    /// Mqtt properties
    /// </summary>
    public InputField consoleInputField;
    private MqttClient client;
    private string broker;
    private int port;
    private bool secure;
    private MqttSslProtocols sslprotocol;
    private MqttProtocolVersion protocolversion;
    private string username;
    private string password;
    private string clientId;
    private string topic_pub_login;
    private string topic_sub_all;
    private string topic_requestTagTnfo;
    private string topic_get_anchors;
    private string topic;
    private bool publish = false;
    private byte qos;
    private bool retain;
    private bool cleansession;
    private ushort keepalive;
    private bool loginSuccess;

    public List<Tag> tagList = new List<Tag>();
    public List<Anchor> anchorList = new List<Anchor>();

    public JObject tagmsg;
    public JObject locationmsg;
    public JObject configmsg;
    public JObject loginmsgresponse;
    public JObject anchormsg;


    public GameObject AnchorContainer;
    public GameObject TagContainer;


    /// <summary>
    /// Data properties
    /// </summary>
    public bool coordinateUpdate;
    public bool loginResponse;
    public bool setupDone;
    public bool requestTagInfo;
    public string requestTagInfo_ID;

    public double x_thresh_low = -100.0;
    public double x_thresh_high = 100.0;
    public double y_thresh_low = -100.0;
    public double y_thresh_high = 100.0;
    public double z_thresh_low = -100.0;
    public double z_thresh_high = 100.0;

    public int anchorcount = 0;
    public int tagCount = 0;

    //msg flags and vars
    public bool tagMsg = false;
    public bool configMsgAnchor = false;
    public bool locationMsg = false;
    public bool spawnTag = false;
    public bool hideTag = false;
    public bool showTag = false;

    public string anchorID;
    public string tagID;

    // vector for the orgin
    public Vector3 originVector;



    public class LoginMsg
    {
        public string user_id { get; set; }
        public string password_id { get; set; }
    }

    public class TagRequestMsg
    {
        public string user_id { get; set; }
        public string password_id { get; set; }
        public string tag_id { get; set; }
    }

    /// <summary>
    /// Menu UI
    /// </summary>
    public LoginHandler login;

    #endregion

    #region Initilization
    /// <summary>
    /// Start is called before the first frame update.
    /// </summary>

    private void Start()
    {

        //Set up default Mqtt properties for https://github.com/khilscher/MqttClient
        broker = "192.168.1.35";
        port = 1883;
        secure = false;
        sslprotocol = MqttSslProtocols.None;
        protocolversion = MqttProtocolVersion.Version_3_1_1;
        username = "test";
        password = "pass";
        System.Random random = new System.Random();
        clientId = random.Next(99999).ToString();
        publish = false;
        qos = (byte)2;
        retain = false;
        cleansession = false;
        keepalive = 60;
        topic_sub_all = "dwm/node/#";
        topic_pub_login = "dwm/holo/login";
        topic_requestTagTnfo = "dwm/holo/requesttaginfo";
        topic_get_anchors = "dwm/holo/requestanchors";

        //Update the settings menu with default values
        login.user_InputField.text = username;
        login.pass_InputField.text = password;
        login.broker_InputField.text = broker;
        login.port_InputField.text = Convert.ToString(port);


        //Default data properties
        loginSuccess = false;
        setupDone = false;
        loginResponse = false;
        coordinateUpdate = false;
        requestTagInfo = false;

        AnchorContainer = Resources.Load("AnchorContainer") as GameObject;
        TagContainer = Resources.Load("TagContainer") as GameObject;

        //Add callback methods for setting ui
        login.ConnectButton.onClick.AddListener(() => Connect());
        login.SetUpButton.onClick.AddListener(() => SetupDone());
    }
    #endregion

    #region Methods


    /*
     * SetupDone() is triggered when the setup done is presson the UI, this is meant to be pressed when all the anchors
     * are loaded in and the user has placed them in AR space accordingly and ready for tags. When pressed this triggers
     * the setup done flag to true.
     *
     * Also from here we must get the orgin anchor (0,0,0) and calculated the offeset vector in AR space. Since the DWM network
     * and the AR space share the same unit of measure (m) then any coordinate recieved by the DWM network for a tag can be plotted
     * in AR with with that coordiante + the offset vector of the origin. This assuming the x,y,z planes are in the same direction,
     * if not I belive we can just match the directions accordinly ie, if z is up in DWM and y is up in AR then the y component of the
     * orgin vector would be added to the z component of the DWM network I THINK - V
     *
     * */
    public void SetupDone()
    {
        // flip the setup done flag to true
        this.setupDone = true;

        try
        {
            // now we must get the orgin achor from the list then create a vector from its position
            Anchor originAnchor = anchorList.FirstOrDefault(a => a.isOriginAnchor == true);
            originVector = originAnchor.clone.GetComponentInChildren<AnchorScript>().anchorVector.position;
            consoleInputField.text += "Setup Done\n";
        }
        catch
        {
            consoleInputField.text += "Zero Vector Error\n";
            this.setupDone = false;
        }


    }

    public Vector3 matrixMath(Tag t)
    {

        var A_Matrix = Matrix<double>.Build.Dense(3, 3); // this will be the temp matrix
        var b_Vector = Vector<double>.Build.Dense(new double[] { t.x, t.y, t.z }); // this will be the b matrix with the tag coords

        double[,] arrayAnchors = new double[3, 3]; // array to add the vectors into the matrix

        int i = 0; // counter for the loop

        // this loops will go through all the anchors
        foreach (Anchor a in anchorList)
        {
            if (!a.isOriginAnchor) // ignore the origin anchor
            {
                arrayAnchors[0, i] = a.clone.GetComponentInChildren<AnchorScript>().anchorVector.position.x - originVector.x; // get anchor coordinate x in holo - the orgin vector
                arrayAnchors[1, i] = a.clone.GetComponentInChildren<AnchorScript>().anchorVector.position.y - originVector.y; // get anchor coordinate y in holo - the orgin vector
                arrayAnchors[2, i] = a.clone.GetComponentInChildren<AnchorScript>().anchorVector.position.z - originVector.z; // get anchor coordinate z in holo - the orgin vector

                A_Matrix.At(0, i, a.x); // get the coordinate x in dwm
                A_Matrix.At(1, i, a.y); // get the coordinate y in dwm
                A_Matrix.At(2, i, a.z); // get the coordinate z in dwm

                i++; // increment counter
            }
        }

        //Debug.Log(A_Matrix.ToString());
        //Debug.Log(b_Vector.ToString());
        //Debug.Log(arrayAnchors.ToString());

        // this solves the system of equations where Ax=b, in terms of x; where x is the coeficents c1, c2, c3
        var x_Vector = A_Matrix.Solve(b_Vector);

        //Debug.Log(x_Vector.ToString());

        double c1 = x_Vector.At(0); // this is the first element in the vector; c1
        double c2 = x_Vector.At(1); // this is the second element in the vector; c2
        double c3 = x_Vector.At(2); // this is the third element in the vecotr; c3

        // do the math, this can be done better but for visualization purposes
        double final_x = (c1 * arrayAnchors[0, 0] + c2 * arrayAnchors[0, 1] + c3 * arrayAnchors[0, 2]) + originVector.x;
        double final_y = (c1 * arrayAnchors[1, 0] + c2 * arrayAnchors[1, 1] + c3 * arrayAnchors[1, 2]) + originVector.y;
        double final_z = (c1 * arrayAnchors[2, 0] + c2 * arrayAnchors[2, 1] + c3 * arrayAnchors[2, 2]) + originVector.z;

        // this is our final vector
        Vector3 final = new Vector3((float)final_x, (float)final_y, (float)final_z);

        return (final);
    }


    /// <summary>
    /// Connect to MySQL and MQTT when Enter button is pushed
    /// </summary>
    public void Connect()
    {
        //Connect to MQTT
        
        MqttConnect();
        //Publsih message to connect to MySQL
        LoginMsg loginmsg = new LoginMsg();
        loginmsg.user_id = this.username;
        loginmsg.password_id = this.password;
        string login_msg = JsonConvert.SerializeObject(loginmsg);
        MqttPublish(this.topic_pub_login, login_msg);
        MqttSubscribe(this.topic_sub_all);
        this.login.LoginConnect();
        Debug.Log("Connect Done");

    }
    /// <summary>
    /// Update is called every frame, if the MonoBehaviour is enabled.
    /// </summary>

    private void Update()
    {
        //if we have new data, update the corresponding text in the scene

        if (loginResponse)
        {
            consoleInputField.text += topic + "\n";
            consoleInputField.text += (string)loginmsgresponse["user_id"] + "\n";
            if ((bool)loginmsgresponse["valid"] == true)
            {
                consoleInputField.text += "Login Correct\n";
                loginSuccess = true;

                string msg = "send anchors";
                MqttPublish(this.topic_get_anchors, JsonConvert.SerializeObject(msg)); // ask for anchors
            }
            else
            {
                consoleInputField.text += "Login Incorrect\n";
            }
            loginResponse = false;
        }
        if (requestTagInfo)
        {
            consoleInputField.text += "tag config recieved \n";
            TagRequestMsg tagrequestmsg = new TagRequestMsg();
            tagrequestmsg.tag_id = requestTagInfo_ID;
            tagrequestmsg.user_id = username;
            tagrequestmsg.password_id = password;
            string tagrequestmsg_str = JsonConvert.SerializeObject(tagrequestmsg);
            MqttPublish(topic_requestTagTnfo, tagrequestmsg_str);
            requestTagInfo = false;
        }
        if (tagMsg)
        {
            //print all tag list members
            consoleInputField.text += "Tag Msg Recieved\n";
            tagMsg = false;
        }
        if (configMsgAnchor)
        {
            //print all anchor list members
            try
            {
                consoleInputField.text += "Anchor Config Msg Recieved\n";
                Anchor anchor = anchorList.FirstOrDefault(a => a.id == anchorID);
                consoleInputField.text += "Anchor ID: " + anchor.id + "\n";
                anchor.InstantiateGameObject(anchorcount);
            }
            catch
            {
                consoleInputField.text += "Anchor Instantiation Error\n";
            }
            configMsgAnchor = false;
        }
        if (locationMsg)
        {
            //print all tag location
            //consoleInputField.text += "Location Msg Recieved\n";

            // if the coords need to be updated
            if (coordinateUpdate)
            {

                // get the tag id and up date the coords
                Tag tag = tagList.FirstOrDefault(obj => obj.id == tagID);

                // check to see if the tag pane is open, if it is dont move it
                if (!tag.clone.GetComponentInChildren<TagScript>().isOpened)
                {
                    tag.UpdateCoords(matrixMath(tag));
                }

                coordinateUpdate = false; // reset the flag
            }

            // if we need to hide the tag
            if (hideTag)
            {
                // get the tag id and up date the coords
                Tag tag = tagList.FirstOrDefault(obj => obj.id == tagID);
                tag.Hide(); // call the hide function
                hideTag = false; // reset the flag

            }

            // if we need to show the tag
            if (showTag)
            {
                // get the tag id and up date the coords
                Tag tag = tagList.FirstOrDefault(obj => obj.id == tagID);
                tag.Show(); // call the show function
                tag.UpdateCoords(originVector); // update the coords so it positions correctly
                showTag = false; // reset the flag

            }

            locationMsg = false; // reset the flag
        }
        if (spawnTag)
        {
            try
            {
                
                consoleInputField.text += "First Tag Location Msg Recieved\n";
                Tag tag = tagList.FirstOrDefault(obj => obj.id == tagID);
                if(!tag.spawned)
                {
                    consoleInputField.text += "Tag ID: " + tag.id + "\n";
                    tag.InstantiateGameObject(matrixMath(tag));
                    tag.spawned = true;
                }

            }
            catch
            {
                consoleInputField.text += "Tag Instantiation Error\n";
            }
            this.spawnTag = false;
        }

    }

    /// <summary>
    /// Updated MQTT based on values in the setting menu.
    /// </summary>
    public void UpdateMqttBasedOnSettingMenu()
    {
        username = login.user_InputField.text;
        password = login.pass_InputField.text;
        broker = login.broker_InputField.text;
        port = Convert.ToInt32(login.port_InputField.text);
    }

    /// <summary>
    /// Connected to Mqtt.
    /// </summary>
    public void MqttConnect()
    {
        try
        {
            //UpdateMqttBasedOnSettingMenu();
            client = new MqttClient(this.broker);

            // Set MQTT version
            client.ProtocolVersion = this.protocolversion;

            // Setup callback for receiving messages
            client.MqttMsgPublishReceived += ClientRecieveMessage;

            // MQTT return codes
            // https://www.hivemq.com/blog/mqtt-essentials-part-3-client-broker-connection-establishment/
            // https://www.eclipse.org/paho/clients/dotnet/api/html/4158a883-de72-1ec4-2209-632a86aebd74.htm
            byte resp = client.Connect(this.clientId); //, this.username, this.password, this.cleansession, this.keepalive);
            if (resp.ToString() == "0")
            {
                this.login.loginSuccess = true;
                this.consoleInputField.text += "Broker Connected\n";
            }
            else
            {
                this.login.loginSuccess = false;
                this.consoleInputField.text += "Broker NOT Connected\n";
            }
        }
        catch (SocketException e)
        {
            //print error message to menu canvas
            this.consoleInputField.text += e.Message + "\n";
        }
        catch (Exception e)
        {
            //print error message to menu canvas
            this.consoleInputField.text += e.Message + "\n";

        }
    }

    /// <summary>
    /// Subscribe to predefined Mqtt topic.
    /// </summary>


    public void MqttSubscribe(string topic)
    {
        if (client != null && client.IsConnected)
        {
            ushort resp = client.Subscribe(
                new string[] { topic },
                new byte[] { this.qos });
            if (resp.ToString() == "2")
            {
                consoleInputField.text += "Subscribe Successful\n";
            }


        }
        else
        {
            this.consoleInputField.text += "Subscribe Unsuccessful\n";

        }

        Debug.Log(topic);
    }

    /// <summary>
    /// Call back Method for recieving messages from MQTT.
    /// </summary>

    public void ClientRecieveMessage(object sender, MqttMsgPublishEventArgs e)
    {
        Debug.Log("MQTT Message");
        Debug.Log(e.Topic);
        this.topic = e.Topic;
        //topic e.g. dwm/node/<tag_ID>/uplink/location
        string[] topic_split = this.topic.Split('/');
        //Tag being sent with DB info from python app

        if (topic_split[2] == "loginresults" && !this.loginSuccess)
        {
            this.loginmsgresponse = JObject.Parse(System.Text.UTF8Encoding.UTF8.GetString(e.Message));
            this.loginResponse = true;
        }
        else if (this.loginSuccess)
        {
            if (topic_split[2] == "tag")
            {
                this.tagmsg = JObject.Parse(System.Text.UTF8Encoding.UTF8.GetString(e.Message));
                Tag tag = new Tag()
                {
                    id = (string)tagmsg["tag"],
                    first_name = (string)tagmsg["first_name"],
                    last_name = (string)tagmsg["last_name"],
                    height = (string)tagmsg["height"],
                    weight = (string)tagmsg["weight"],
                    sex = (string)tagmsg["sex"],
                    pic = (string)tagmsg["pic"],
                    spawned = false,
                    outOfRange = false,
                    x = 0.0,
                    y = 0.0,
                    z = 0.0,
                    tagObj = TagContainer
                };
                this.tagCount++;
                tagList.Add(tag);
                this.tagMsg = true;

            }
            /*
            else if (topic_split[2] == "anchors")
            {
                this.anchormsg = JObject.Parse(System.Text.UTF8Encoding.UTF8.GetString(e.Message));
                while (this.configMsgAnchor)
                {

                }
                string anchorid = ((string)this.anchormsg["configuration"]["label"]).Substring(2);

                Anchor anchor = new Anchor()
                {
                    id = anchorid,
                    x = (double)this.anchormsg["configuration"]["anchor"]["position"]["x"],
                    y = (double)this.anchormsg["configuration"]["anchor"]["position"]["y"],
                    z = (double)this.anchormsg["configuration"]["anchor"]["position"]["z"],
                    anchorObj = AnchorContainer
                };
                this.anchorID = anchorid;
                this.anchorcount++;
                this.anchorList.Add(anchor);
                this.configMsgAnchor = true;
            }
            */
            else if (topic_split[3] == "uplink")
            {
                if (topic_split[4] == "location")
                {
                    try
                    {
                        this.locationmsg = JObject.Parse(System.Text.UTF8Encoding.UTF8.GetString(e.Message));
                        Tag tag = tagList.FirstOrDefault(obj => obj.id == topic_split[2]);

                        // only do these check if the setup done
                        if (this.setupDone)
                        {
                            // first check to see if we already spawned the tag and it is not out of range
                            if (tag.spawned && !tag.outOfRange)
                            {
                                // check to see if the tag is out of range, if it is see below (i think these are ORs since if it breaks any then it disappears, right?)
                                if (
                                    ((double)locationmsg["position"]["x"] < this.x_thresh_low || (double)locationmsg["position"]["x"] > this.x_thresh_high) ||
                                    ((double)locationmsg["position"]["y"] < this.y_thresh_low || (double)locationmsg["position"]["y"] > this.y_thresh_high) ||
                                    ((double)locationmsg["position"]["z"] < this.z_thresh_low || (double)locationmsg["position"]["z"] > this.z_thresh_high)
                                    )
                                {
                                    this.tagID = tag.id; // get the tag id
                                    this.locationMsg = true; // flip the location message flag since this is a location message
                                    this.hideTag = true; // flip the hide tag flag to true so we can call the function in the update method
                                    tag.outOfRange = true;// now also flip the out of range flag inside the class itself.
                                }

                                // so if its not out of range then its a normal update of the coords
                                else
                                {
                                    tag.x = (double)locationmsg["position"]["x"];
                                    tag.y = (double)locationmsg["position"]["y"];
                                    tag.z = (double)locationmsg["position"]["z"];
                                    this.tagID = tag.id; // get the tag id
                                    this.locationMsg = true; // flip the location message flag since this is a location message
                                    this.coordinateUpdate = true; // now flip the update coords flags so we can call it from the update method
                                }
                            }

                            // now check if the tag is not spawned, and in range (redundant maybe?)
                            else if (!tag.spawned && !tag.outOfRange)
                            {
                                // act as a buffer while spawning the the tag i think
                                while (this.spawnTag)
                                {

                                }
                                // set the stuff to spawn the tag with the coords
                                tag.x = (double)locationmsg["position"]["x"];
                                tag.y = (double)locationmsg["position"]["y"];
                                tag.z = (double)locationmsg["position"]["z"];
                                this.tagID = topic_split[2]; // get the id
                                this.spawnTag = true; // flip to spawn tag
                            }
                            // now if the tag is in out of reange
                            else if (tag.outOfRange)
                            {
                                //check to see if it came back and if so see below
                                if (
                                     ((double)locationmsg["position"]["x"] > this.x_thresh_low && (double)locationmsg["position"]["x"] < this.x_thresh_high) &&
                                     ((double)locationmsg["position"]["y"] > this.y_thresh_low && (double)locationmsg["position"]["y"] < this.y_thresh_high) &&
                                     ((double)locationmsg["position"]["z"] > this.z_thresh_low && (double)locationmsg["position"]["z"] < this.z_thresh_high)
                                     )
                                {
                                    //get the coords to put it back on the screen
                                    tag.x = (double)locationmsg["position"]["x"];
                                    tag.y = (double)locationmsg["position"]["y"];
                                    tag.z = (double)locationmsg["position"]["z"];
                                    tag.outOfRange = false; // tag is now back in range so make this false
                                    this.tagID = tag.id; // get the tag id
                                    this.locationMsg = true; // flip the location message flag since this is a location message
                                    this.showTag = true; // we have to show the tag now, so turn this on

                                }
                            }
                        }

                    }
                    catch
                    {
                        //Debug.Log("Location Error");

                    }
                }

                else if (topic_split[4] == "config")
                {
                    this.configmsg = JObject.Parse(System.Text.UTF8Encoding.UTF8.GetString(e.Message));
                    if ((string)this.configmsg["configuration"]["nodeType"] == "ANCHOR")
                    {
                        while (this.configMsgAnchor)
                        {

                        }
                        Anchor anchor = new Anchor()
                        {
                            id = topic_split[2],
                            x = (double)this.configmsg["configuration"]["anchor"]["position"]["x"],
                            y = (double)this.configmsg["configuration"]["anchor"]["position"]["y"],
                            z = (double)this.configmsg["configuration"]["anchor"]["position"]["z"],
                            anchorObj = AnchorContainer
                        };
                        this.anchorID = topic_split[2];
                        this.anchorcount++;
                        this.anchorList.Add(anchor);
                        this.configMsgAnchor = true;

                    }
                    
                    if((string)this.configmsg["configuration"]["nodeType"] != "ANCHOR")
                    {
                        this.requestTagInfo_ID = topic_split[2];
                        this.requestTagInfo = true;

                    }

                }

            }

        }
    }

    /// <summary>
    /// Disconnect from Mqtt broker.
    /// </summary>

    private void MqttDisconnect()
    {
        if (client != null && client.IsConnected)
        {
            client.Disconnect();
            //settings.DebugConsole.text = "Disconnect()";
        }
        else
        {
            //settings.DebugConsole.text = "Not connected";
        }
    }

    /// <summary>
    /// Unsubscribe from Mqtt topic.
    /// </summary>
    public void MqttUnsubscribe()
    {
        if (client != null && client.IsConnected)
        {
            // ushort resp = client.Unsubscribe(
            //new string[] { this.topic });

            //settings.DebugConsole.text = "Unsubscribe() Response: " + resp.ToString();
        }
        else
        {
            //settings.DebugConsole.text = "Not connected";

        }
    }


    public void MqttPublish(string topic, string msg)
    {

        client.Publish(topic, System.Text.Encoding.UTF8.GetBytes(msg), this.qos, this.retain);
        this.consoleInputField.text += "Message Published\n";
        Debug.Log(topic);
        Debug.Log(msg + " Published");
    }

    public void ClearConsole()
    {
        consoleInputField.text = "";
    }
    #endregion
}
