using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Linq;
using System.Net.Sockets;
using System.Windows;
using TMPro;
using UnityEngine;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using System.Collections;
using System.Collections.Generic;

using UnityEngine.UI;


public class Tag : MonoBehaviour
{
    public string id { get; set; }
    public string first_name { get; set; }
    public string last_name { get; set; }
    public string height { get; set; }
    public string weight { get; set; }
    public string sex { get; set; }
    public string pic { get; set; }
    public bool spawned { get; set; }
    public bool outOfRange { get; set; }
    public double x { get; set; }
    public double y { get; set; }
    public double z { get; set; }

    private double x_pos;

    public GameObject tagObj;
    public GameObject clone; // the way we will reference the instance of the tagObj (aka the resource loaded from before) 
    public float speed = 1f;
    
    //public MatrixMath matrixmath = new MatrixMath();

    public void InstantiateGameObject(Vector3 posVector)//List<Anchor> anchorList)
    {
      
        clone = Instantiate<GameObject>(tagObj, posVector, Quaternion.identity);

        clone.GetComponentInChildren<TagScript>().writeTag(id, first_name, last_name, height, weight, sex, pic);

    }

    // here we will pass the origin vecotor (to offset) and the new coords then set the clone (instance) to the new position.
    public void UpdateCoords(Vector3 posVector)
    {
        // smoothed movement
        //float step = speed * Time.deltaTime;
        clone.transform.position = Vector3.Lerp(clone.transform.position, posVector, .25f);

        // Rotation(tag faces user)
        Vector3 cameraForward = Camera.main.transform.forward;
        Quaternion targetRotation = Quaternion.LookRotation(cameraForward, Vector3.up);
        clone.transform.rotation = Quaternion.Lerp(clone.transform.rotation, targetRotation, .25f);
    }

    public void Hide()
    {
       // clone.SetActive(false); // Simple as that!
    }

    public void Show()
    {
        clone.SetActive(true); // Simple as that!
    }
    
    

}