package json;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class JsonController {

	private static JsonController uniqueInstance;
	
	 JSONParser jsonParser;
	 Map<String, JSONObject> totalJsonObjMap = new HashMap<>();

	 
	/*»ý¼ºÀÚ*/
	public JsonController(){
		
		jsonParser = new JSONParser();
	}
	
	// Lazy Initailization
    public static  JsonController getInstance() {
      if(uniqueInstance == null) {
         uniqueInstance = new JsonController();
      }
      return uniqueInstance;
    }
    
	/*read json*/
	public int readJson(String fileName) throws Exception {
		
		int returnVal = 0;
		
		if (fileName != null && fileName.length() > 0) {
			String totalPath = System.getProperty("user.dir");
			totalPath += "/json/" + fileName;
					
			
  		  Object obj = jsonParser.parse(new FileReader(totalPath));
  		  JSONObject totalJsonObject = (JSONObject)obj;
  		  
  		  if (totalJsonObject != null) {
  		   	returnVal = 1;
  		    totalJsonObjMap.put(fileName, totalJsonObject);
  		  }
		}
		
		return returnVal;
	}
	
	/*get json object*/
	public JSONObject getTotalJsonObject(String fileName) {
		
		return totalJsonObjMap.get(fileName);
	}
	
	
	/*write json*/
	public void writeJson(String path, String fileName) throws Exception {
		
		JSONObject totalJsonObject = totalJsonObjMap.get(fileName); 
		
		 if (totalJsonObject != null) {
			 
			 String totalPath = path  + fileName;
			 
			 try (FileWriter file = new FileWriter(totalPath)) {
		            file.write(totalJsonObject.toJSONString());
		        } catch (IOException e) {
		            e.printStackTrace();
		        }
			 
		 }		
	}
	
	/*write json with other target*/
	public void writeJson(String path, String fileName, JSONObject target) throws Exception {
		
		 if (target != null) {
			 
			 String totalPath = path  + fileName;
			 
			 try (FileWriter file = new FileWriter(totalPath)) {
		            file.write(target.toJSONString());
		        } catch (IOException e) {
		            e.printStackTrace();
		        }
			 
		 }		
	}
}
