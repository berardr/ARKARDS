using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Microsoft.MixedReality.Toolkit.Experimental.Utilities;
using UnityEngine.XR.WSA;
using UnityEngine.XR.WSA.Persistence;
using TMPro;
using UnityEngine.UI;

public class AnchorScript : MonoBehaviour
{
    public Rigidbody rb;
    public SpriteRenderer spriteRenderer;

    public Sprite sprite1;
    public Sprite sprite2;

    public TextMeshProUGUI ID_label;
    public TextMeshProUGUI x_label;
    public TextMeshProUGUI y_label;
    public TextMeshProUGUI z_label;

    public Transform anchorVector;
    public Transform lockVector;

    

    private int i = 0;

    public void AnchorIt()
    {
        rb.constraints = RigidbodyConstraints.FreezePositionX | RigidbodyConstraints.FreezePositionZ | RigidbodyConstraints.FreezePositionY;
        spriteRenderer.sprite = sprite1;
    }

    public void ReleaseAnchor()
    {
        rb.constraints = RigidbodyConstraints.None;
        rb.constraints = RigidbodyConstraints.FreezeRotationX | RigidbodyConstraints.FreezeRotationZ | RigidbodyConstraints.FreezeRotationY;
        spriteRenderer.sprite = sprite2;
    }

    public void HandleAnchor()
    {
        if (i == 0)
        {
            AnchorIt();
            i = 1;
        }
        else
        {
            ReleaseAnchor();
            i = 0;
        }
    }

    public void setAnchor(double x_cord, double y_cord, double z_cord, string id)
    {
        x_label.text = x_cord.ToString("F");
        y_label.text = y_cord.ToString("F");
        z_label.text = z_cord.ToString("F");

        ID_label.text = id;
        transform.parent.name = id;

  
    }
}
