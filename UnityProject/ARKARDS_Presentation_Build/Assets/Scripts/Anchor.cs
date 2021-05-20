
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


public class Anchor : Mqttmanager_ARK
{
    public string id { get; set; }
    public double x { get; set; }
    public double y { get; set; }
    public double z { get; set; }
    private double x_pos;
    public GameObject anchorObj;
    public Component[] Labels;
    public Component x_component;
    public Component y_component;
    public Component z_component;

    public GameObject clone; // this is maybe the way to refrence the clone made in AR???

    public bool isOriginAnchor = false; // true if the achor is the orgin of the DWM system

    public void InstantiateGameObject(int n)
    {
        x_pos = .1 + (n * .15);
        clone = Instantiate(anchorObj, new Vector3(0, 0, 0), Quaternion.identity);

        clone.GetComponentInChildren<AnchorScript>().anchorVector.position += new Vector3((float)x_pos, (float)-.25, (float).5);
        clone.GetComponentInChildren<AnchorScript>().lockVector.position += new Vector3((float)x_pos, (float)-.25, (float).5);

        clone.GetComponentInChildren<AnchorScript>().setAnchor(x, y, z, id);

        // check to see if the anchor is the origin of the DWM system, if it is set flag to true
        if (x == 0 && y == 0 && z == 0)
        {
            isOriginAnchor = true;
        }

    }

}