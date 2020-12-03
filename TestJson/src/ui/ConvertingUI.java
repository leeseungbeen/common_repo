package ui;

import java.awt.Container;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import json.IConvertingJson;
import json.TiledToTrivaso;

public class ConvertingUI extends JFrame {

	 private static final long serialVersionUID = -711163588504124217L;

	 private ArrayList<IConvertingJson> convertingInstArr = new ArrayList<IConvertingJson>();
	 private IConvertingJson curConvertingInst = null;
	 
	 public ConvertingUI() {
		 
		  super("converting ui");
		 
		  convertingInstArr.add(new TiledToTrivaso());
		  
		  setBounds(100 , 100 , 400 , 200);
		  setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		  
		  Container contentPane = this.getContentPane();
		  JPanel pane = new JPanel();
		  JButton buttonStart = new JButton("Start");
		  final JTextField textPeriod = new JTextField(20);
		  final JTextField textResultPeriod = new JTextField(20);
		  JLabel labelTargetPath = new JLabel("Input Target Name : ");
		  JLabel labelResultPath = new JLabel("Input Result Name : ");
		  JCheckBox checkboxIsRandom = new JCheckBox("is Traviso    ");
		 
		  textPeriod.setText("test_r_1_result.json");
		  textResultPeriod.setText("test_r_1_result_complete.json");
		  
		  String filePath = System.getProperty("user.dir") + "/json/";
		  JLabel labelFilePath = new JLabel("File Path : " + filePath);
		  		  
		  buttonStart.addActionListener(new ActionListener(){ //익명클래스로 리스너 작성
				public void actionPerformed(ActionEvent e){
					
					if (curConvertingInst != null) {
						
						curConvertingInst.convertingJson(filePath, textPeriod.getText(), textResultPeriod.getText());
					}
					
				}
			});
		  
		  checkboxIsRandom.addChangeListener(new ChangeListener() {
		   
		   @Override
		   public void stateChanged(ChangeEvent e) {
			   
		    if(((JCheckBox)e.getSource()).isSelected())
		    {		    			    	
		    	curConvertingInst = convertingInstArr.get(0);
		    
		    }else
		    {
		    	if (convertingInstArr.size() > 1) {
		    		curConvertingInst = convertingInstArr.get(1);	
		    	}
		    	
		    }
		   }
		  });
		  
		  checkboxIsRandom.setSelected(true);
		  
		  buttonStart.setMnemonic('S');
		  
		  
		  pane.add("North",labelFilePath);
		  
		  pane.add(labelTargetPath);
		  pane.add(textPeriod);
		  pane.add(labelResultPath);
		  pane.add(textResultPeriod);
		  pane.add(checkboxIsRandom);
		  pane.add(buttonStart);
		  contentPane.add(pane);
		  
		  
		  setVisible(true);
	 }
		
}
