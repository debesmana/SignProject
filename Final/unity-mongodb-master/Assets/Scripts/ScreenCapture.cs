using UnityEngine;
using System.Collections;
using System;

//Allows you to take an image of the screen
public class ScreenCapture : MonoBehaviour {

	public RenderTexture overviewTexture;
	GameObject OVcamera;
	public string path = "";

	// Use this for initialization
	void Start () {
		//use render camera
		OVcamera = GameObject.FindGameObjectWithTag("RenderCamera");
	}
	

	// Update is called once per frame
	void LateUpdate () {
		if (Input.GetKeyDown( KeyCode.Return ))
		{
			Debug.Log("Screenshot taken");
			//Multithreading since writing screenshot to memory might take a long time
			StartCoroutine(TakeScreenShot());
		}
	}

	//return file name that your photo is going to be called
	string fileName()
	{
		return string.Format("screen_{0}.png", 
		System.DateTime.Now.ToString("yyyy-MM-dd_HH-mm-ss"));

	}

	public IEnumerator TakeScreenShot()
	{
		yield return new WaitForEndOfFrame();

		Camera camOV = OVcamera.GetComponent<Camera>();
		//taking the GameObjects camera

		RenderTexture currentRT = RenderTexture.active;
		//currentRT is the active RenderTexture in use

		RenderTexture.active = camOV.targetTexture;
		//Sets the active RenderTexture to the one assigned to the camera
		camOV.Render();
		Texture2D imageOverview = new Texture2D(camOV.targetTexture.width, camOV.targetTexture.height,TextureFormat.RGB24, false);
		imageOverview.ReadPixels(new Rect(0, 0, camOV.targetTexture.width, camOV.targetTexture.height), 0, 0);
		imageOverview.Apply();
		RenderTexture.active = currentRT;

		//Encode texture into png
		byte[] bytes = imageOverview.EncodeToPNG();

		//save in memory
		string filename = fileName();
		path = Application.persistentDataPath + "/Snapshots/" + filename;

		//opens file, writes to it, closes it
		System.IO.File.WriteAllBytes(path, bytes);

		Debug.Log("Saved to " + path);

	}
}
