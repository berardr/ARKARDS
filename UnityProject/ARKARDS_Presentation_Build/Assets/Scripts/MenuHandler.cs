using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class MenuHandler : MonoBehaviour
{
    public GameObject MQTT_Menu;
    public GameObject Login_Menu;

    public bool mqtt_togl = true;
    public bool login_togl = true;

    
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void toggleMQTT()
    {
        if (mqtt_togl)
        {
            MQTT_Menu.SetActive(false);
            mqtt_togl = false;
        }
        else
        {
            MQTT_Menu.SetActive(true);
            mqtt_togl = true;
        }
    }

    public void toggleLogin()
    {
        if (login_togl)
        {
            Login_Menu.SetActive(false);
            login_togl = false;
        }
        else
        {
            Login_Menu.SetActive(true);
            login_togl = true;
        }
    }
}
