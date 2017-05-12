using UnityEngine;
using UnityEngine.UI;
using System; //
using System.Collections;
using System.Collections.Generic;  // Lists

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Driver.Builders;  
using MongoDB.Driver.GridFS;  
using MongoDB.Driver.Linq; 

public class RetrievePoems : MonoBehaviour {
	
	private string connectionString;

	[SerializeField] private bool USE_LOCAL = true;
	[SerializeField] private string mongoUsername;
	[SerializeField] private string mongoPassword;
	[SerializeField] private int numOfPoemsDrawn;
	
	[SerializeField] private Text poemOutputText;
	public static string daina;

	

	// Use this for initialization
	void Start () {

		if (USE_LOCAL){
			connectionString = "mongodb://localhost:27017";
		}
		else {
			connectionString = "mongodb://" + mongoUsername + ":" + mongoPassword + "@mongoserver.almaulmane.com:27067/";
		}

		/*
		 * 1. establish connection
		 */

		var client = new MongoClient(connectionString);
		var server = client.GetServer(); 
		var database = server.GetDatabase("poems");
		var poemcollection= database.GetCollection<BsonDocument>("poems");
		Debug.Log ("1. ESTABLISHED CONNECTION");

		/*
		 * 2. SELECT all daina FROM poems
		 */

		/*foreach (var document in poemcollection.FindAll()) {
			Debug.Log("2. SELECT ALL DOCS: \n" + document["daina"]);
		}*/

		/*
		 * 3. COUNT docs in database
		 */

		 int poemAmount = (int)poemcollection.Count();
		 Debug.Log("3. COUNT DOCS: \n" + poemAmount);

		/*
		 * 4. DRAW random daina to project
		 */

		for (int i = 0; i < numOfPoemsDrawn; i++)
		{
			int rand = UnityEngine.Random.Range(0, poemAmount);
			foreach (var poemToDraw in poemcollection.Find(new QueryDocument("poemNumber", rand)))
			{
				Debug.Log("4. DRAW random daina: \n" + poemToDraw["daina"]);
				string tempVar = poemToDraw["daina"].ToString().Replace(" | ", "\n");
				daina = tempVar;
				poemOutputText.text += tempVar;
				poemOutputText.text += "\n\n";
			}
		}
	
	}
	
	// Update is called once per frame
	void Update () {
	
	}
}
 