package org.davidliebman.tag;

import com.intellij.openapi.components.BaseComponent;
import com.intellij.openapi.components.ComponentConfig;
import com.intellij.openapi.components.ServiceManager;
import com.intellij.openapi.components.*;

import com.intellij.openapi.extensions.ExtensionPointName;
import com.intellij.openapi.fileChooser.FileChooserDescriptor;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.ui.TextFieldWithBrowseButton;
import com.intellij.openapi.util.Condition;
import com.intellij.openapi.util.Key;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.pom.PomModel;
import com.intellij.psi.search.GlobalSearchScope;
import com.intellij.util.messages.MessageBus;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;
import java.awt.*;

/**
 * Created by dave on 2/19/16.
 */
public class ATAGShowImage {
    private JLabel databaseRoot;
    private JLabel splitFolderName;
    private JLabel csvFileSingle;
    private JLabel csvFileSecond;
    private JLabel localDatabase;
    private JLabel csvFileLocal;
    private JLabel programName;
    private JPanel imagePanel;
    private JPanel formPanel; // do not instantiate!!

    /*
    private TextFieldWithBrowseButton textFieldWithBrowseButtonProgram;
    private TextFieldWithBrowseButton textFieldWithBrowseDatabaseRoot;
    private TextFieldWithBrowseButton textFieldWithBrowseSplitDir;
    private TextFieldWithBrowseButton textFieldWithBrowseCsvSingle;
    private TextFieldWithBrowseButton textFieldWithBrowseCsvSecond;
    private TextFieldWithBrowseButton textFieldWithBrowseDatabaseLocal;
    private TextFieldWithBrowseButton textFieldWithBrowseCsvLocal;
    */

    private ATAG var;

    //JFrame frame ;//= new JFrame("ATAGShowImage");


    private void createUIComponents() {
        // TODO: place custom component creation code here
        databaseRoot = new JLabel();
        splitFolderName = new JLabel();
        csvFileSingle = new JLabel();
        csvFileSecond = new JLabel();
        csvFileLocal = new JLabel();
        localDatabase = new JLabel();
        programName = new JLabel();
        imagePanel = new JPanel();
        //formPanel = new JPanel();
        setValues(new ATAG());
        /*
        textFieldWithBrowseButtonProgram = new TextFieldWithBrowseButton();
        textFieldWithBrowseCsvLocal = new TextFieldWithBrowseButton();
        textFieldWithBrowseCsvSecond = new TextFieldWithBrowseButton();
        textFieldWithBrowseCsvSingle = new TextFieldWithBrowseButton();
        textFieldWithBrowseDatabaseLocal = new TextFieldWithBrowseButton();
        textFieldWithBrowseDatabaseRoot = new TextFieldWithBrowseButton();
        textFieldWithBrowseSplitDir = new TextFieldWithBrowseButton();


        FileChooserDescriptor filesOnly = new FileChooserDescriptor(true, false,false,false,false,false);
        FileChooserDescriptor foldersOnly = new FileChooserDescriptor(false,true, false, false, false, false);

        textFieldWithBrowseSplitDir.addBrowseFolderListener(" "," ", new ATAGProject(), foldersOnly);
        textFieldWithBrowseButtonProgram.addBrowseFolderListener(" "," ", new ATAGProject(), filesOnly);
        textFieldWithBrowseDatabaseRoot.addBrowseFolderListener(" "," ", new ATAGProject(), foldersOnly);
        textFieldWithBrowseDatabaseLocal.addBrowseFolderListener(" "," ", new ATAGProject(), foldersOnly);
        textFieldWithBrowseCsvLocal.addBrowseFolderListener(" "," ", new ATAGProject(),filesOnly);
        textFieldWithBrowseCsvSecond.addBrowseFolderListener(" "," ", new ATAGProject(), filesOnly);
        textFieldWithBrowseCsvSingle.addBrowseFolderListener(" "," ", new ATAGProject(), filesOnly);
        */
    }

    private void setDisplayText() {
        if(var == null) return;
        databaseRoot.setText(var.configRootDatabase);
        splitFolderName.setText(var.configSplitFolderName);
        csvFileSingle.setText(var.configCsvFileSingle);
        csvFileSecond.setText(var.configCsvSecond);
        csvFileLocal.setText(var.configCsvLocal);
        localDatabase.setText(var.configLocalRoot);
        programName.setText("TAG");
        System.out.println(databaseRoot.getText());
    }


    public void setValues(ATAG v) {
        var = v;
        setDisplayText();

        try {

            var.selectFile(new ATAGProject());
        }
        catch (Exception e) {e.printStackTrace();}
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("ATAGShowImage");
        frame.setContentPane(new ATAGShowImage().formPanel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);
    }

    /*
    class ATAGComponent extends ServiceManager {

        public ATAGComponent ( ) {

        }

    }
    */


}
