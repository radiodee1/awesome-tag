package org.davidliebman.tag;

import com.intellij.openapi.components.BaseComponent;
import com.intellij.openapi.components.ComponentConfig;
import com.intellij.openapi.extensions.ExtensionPointName;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.util.Condition;
import com.intellij.openapi.util.Key;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.pom.PomModel;
import com.intellij.psi.search.GlobalSearchScope;
import com.intellij.util.messages.MessageBus;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/**
 * Created by dave on 2/19/16.
 */
public class ATAGProject implements Project {

    @Nullable
    public VirtualFile getProjectFile() {
        return null;
    }

    @Nullable
    public VirtualFile getWorkspaceFile() {
        return null;
    }

    @NotNull
    public String getProjectFilePath() {
        return null;
    }

    @Nullable
    public VirtualFile getBaseDir() {
        return null;
    }

    @NotNull
    public String getName() {
        return null;
    }

    @Nullable
    public String getPresentableUrl() {
        return null;
    }

    @NotNull
    public String getLocationHash() {
        return null;
    }

    @NotNull
    public String getLocation() {
        return null;
    }

    public void save() {

    }

    public BaseComponent getComponent(String s) {
        return null;
    }

    public <T> T getComponent(Class<T> aClass) {
        return null;
    }

    public <T> T getComponent(Class<T> aClass, T t) {
        return null;
    }

    @NotNull
    public Class[] getComponentInterfaces() {
        return new Class[0];
    }

    public boolean hasComponent(@NotNull Class aClass) {
        return false;
    }

    @NotNull
    public <T> T[] getComponents(Class<T> aClass) {
        return null;
    }

    @NotNull
    public org.picocontainer.PicoContainer getPicoContainer() {
        return null;
    }

    public MessageBus getMessageBus() {
        return null;
    }

    public boolean isDisposed() {
        return false;
    }

    @NotNull
    public ComponentConfig[] getComponentConfigurations() {
        return new ComponentConfig[0];
    }

    @Nullable
    public Object getComponent(ComponentConfig componentConfig) {
        return null;
    }

    public <T> T[] getExtensions(ExtensionPointName<T> extensionPointName) {
        return null;
    }

    public ComponentConfig getConfig(Class aClass) {
        return null;
    }

    public Condition getDisposed() {
        return null;
    }

    public boolean isOpen() {
        return false;
    }

    public boolean isInitialized() {
        return false;
    }

    public boolean isDefault() {
        return false;
    }

    @NotNull
    public PomModel getModel() {
        return null;
    }

    public GlobalSearchScope getAllScope() {
        return null;
    }

    public GlobalSearchScope getProjectScope() {
        return null;
    }

    public void dispose() {

    }

    public <T> T getUserData(Key<T> key) {
        return null;
    }

    public <T> void putUserData(Key<T> key, T t) {

    }
}
