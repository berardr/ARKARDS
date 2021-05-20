//
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License. See LICENSE in the project root for license information.
//
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using System.Drawing;
using System.IO;
using System;



    public class TagScript : MonoBehaviour
    {
        public static TagScript ActiveTag;

        
        public TextMesh WearerName;
        public TextMesh TagID;

        public Image wearerImage;
        public Text DataTagID;
        public Text DataName;
        public Text DataHeight;
        public Text DataWeight;
        public Text DataSex;

        public Sprite imageSprite;

        public Renderer BoxRenderer;
        public MeshRenderer[] PanelSides;
        public MeshRenderer PanelFront;
        public MeshRenderer PanelBack;
        public MeshRenderer[] InfoPanels;
        public MeshRenderer FlipButton;

        public Material clearance_mat;
        public Material denial_mat;
        public bool tog_mat = false;    

        private BoxCollider boxCollider;
        private PresentToPlayer present;

        // check if the tag is opened.
        public bool isOpened;

        public void SetActiveTag()
        {
            TagScript tag = gameObject.GetComponent<TagScript>();
            ActiveTag = tag;
        }

        public void ResetActiveTag()
        {
            ActiveTag = null;
        }

        public void Start()
        {
            // Turn off our animator until it's needed
            GetComponent<Animator>().enabled = false;
            BoxRenderer.enabled = true;
            present = GetComponent<PresentToPlayer>();
        }

        public void Update()
        {
            //calls every frame to update position of tag based on real world crosss-referenced with unity coordinates
        }

        public void Open()
        {
            if (present.Presenting)
                return;

            StartCoroutine(UpdateActive());
        }

        public void FlipColor()
        {
            Material switch_mat;
            if (!tog_mat)
            {
                switch_mat = clearance_mat;
                FlipButton.material = denial_mat;
            }
            else 
            {
                switch_mat = denial_mat;
                FlipButton.material = clearance_mat;
            }
            tog_mat = !tog_mat;

            for (int i = 0; i < PanelSides.Length; i++)
            {
                PanelSides[i].material = switch_mat;
            }
            for (int i = 0; i < InfoPanels.Length; i++)
            {
                InfoPanels[i].material = switch_mat;
            }
            PanelBack.material = switch_mat;
            PanelFront.material = switch_mat;
            BoxRenderer.material = switch_mat;
        }
        
        public IEnumerator UpdateActive()
        {
            present.Present();

            while (!present.InPosition)
            {
                // Wait for the item to be in presentation distance before animating
                yield return null;
            }

            // Start the animation
            Animator animator = gameObject.GetComponent<Animator>();
            animator.enabled = true;
            animator.SetBool("Opened", true);
            isOpened = true; // change bool for our check

            //Color elementNameColor = ElementName.GetComponent<MeshRenderer>().material.color;

            while (TagScript.ActiveTag == this)
            {
                //ElementName.GetComponent<MeshRenderer>().material.color = elementNameColor;
                // Wait for the player to send it back
                yield return null;
            }

            animator.SetBool("Opened", false);
            isOpened = false; // change bool for our check

            yield return new WaitForSeconds(0.66f); // TODO get rid of magic number        

            // Return the item to its original position
            present.Return();
            //Dim();
        }

        public void base64ToSprite(string base64String)
        {

            byte[] byteArray = Convert.FromBase64String(base64String);

            Texture2D tex = new Texture2D(2, 2);
            tex.LoadImage(byteArray);
            imageSprite = Sprite.Create(tex, new Rect(0.0f, 0.0f, tex.width, tex.height), new Vector2(0.5f, 0.5f), 100.0f);

            wearerImage.sprite = imageSprite;

    }

        public void writeTag (string id, string first_name, string last_name, string height, string weight, string sex, string pic)
        {

            string fullName = first_name + " " + last_name;
            string fullNameNewLine = first_name + "\n" + last_name;

            base64ToSprite(pic);
            WearerName.text = fullNameNewLine;
            TagID.text = id;
            DataTagID.text = id;
            DataName.text = fullName;
            DataHeight.text = height;
            DataWeight.text = weight;
            DataSex.text = sex;
            transform.parent.name = id;

        }

       
    }

