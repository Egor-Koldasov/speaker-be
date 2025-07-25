import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from 'convex/react';
import { api } from '../../convex/_generated/api.js';
import { useAuth } from '@/hooks/useAuth';
import Button from '@/components/ui/Button';
import { Colors } from '@/constants/Colors';

export default function ProfileScreen(): JSX.Element {
  const { signOut } = useAuth();
  const [isSigningOut, setIsSigningOut] = useState(false);
  
  // Get current user data
  const currentUser = useQuery(api.users.getCurrentUser);

  const handleSignOut = async (): Promise<void> => {
    Alert.alert(
      'Sign Out',
      'Are you sure you want to sign out?',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Sign Out',
          style: 'destructive',
          onPress: async () => {
            setIsSigningOut(true);
            await signOut();
            setIsSigningOut(false);
          },
        },
      ]
    );
  };

  const menuItems = [
    {
      id: 'edit-profile',
      title: 'Edit Profile',
      icon: 'person-outline',
      action: () => {
        Alert.alert('Coming Soon', 'Profile editing will be available in a future update.');
      },
    },
    {
      id: 'preferences',
      title: 'Preferences',
      icon: 'settings-outline',
      action: () => {
        Alert.alert('Coming Soon', 'Preferences will be available in a future update.');
      },
    },
    {
      id: 'notifications',
      title: 'Notifications',
      icon: 'notifications-outline',
      action: () => {
        Alert.alert('Coming Soon', 'Notification settings will be available in a future update.');
      },
    },
    {
      id: 'privacy',
      title: 'Privacy & Security',
      icon: 'shield-outline',
      action: () => {
        Alert.alert('Coming Soon', 'Privacy settings will be available in a future update.');
      },
    },
    {
      id: 'help',
      title: 'Help & Support',
      icon: 'help-circle-outline',
      action: () => {
        Alert.alert('Help & Support', 'For support, please contact us at support@langtools.com');
      },
    },
    {
      id: 'about',
      title: 'About',
      icon: 'information-circle-outline',
      action: () => {
        Alert.alert(
          'About Langtools',
          'Langtools v1.0.0\n\nA modern language learning platform powered by AI.\n\n© 2024 Langtools'
        );
      },
    },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>Profile</Text>
        </View>

        {/* User Card */}
        <View style={styles.userCard}>
          <View style={styles.avatarContainer}>
            <View style={styles.avatar}>
              <Ionicons name="person" size={32} color={Colors.primary} />
            </View>
          </View>
          <View style={styles.userInfo}>
            <Text style={styles.userName}>
              {(currentUser && 'name' in currentUser) ? currentUser.name || 'User' : 'User'}
            </Text>
            <Text style={styles.userEmail}>
              {(currentUser && 'email' in currentUser) ? currentUser.email : 'user@example.com'}
            </Text>
          </View>
        </View>

        {/* Menu Items */}
        <View style={styles.menuSection}>
          {menuItems.map((item) => (
            <TouchableOpacity
              key={item.id}
              style={styles.menuItem}
              onPress={item.action}
              activeOpacity={0.7}
            >
              <View style={styles.menuItemContent}>
                <View style={styles.menuItemIcon}>
                  <Ionicons 
                    name={item.icon as any} 
                    size={24} 
                    color={Colors.primary} 
                  />
                </View>
                <Text style={styles.menuItemText}>{item.title}</Text>
              </View>
              <Ionicons 
                name="chevron-forward" 
                size={20} 
                color={Colors.tertiaryLabel} 
              />
            </TouchableOpacity>
          ))}
        </View>

        {/* Sign Out Button */}
        <View style={styles.signOutSection}>
          <Button
            title="Sign Out"
            onPress={handleSignOut}
            variant="outline"
            loading={isSigningOut}
            disabled={isSigningOut}
            style={styles.signOutButton}
            textStyle={styles.signOutButtonText}
          />
        </View>

        {/* App Info */}
        <View style={styles.appInfo}>
          <Text style={styles.appInfoText}>
            Langtools Mobile App v1.0.0
          </Text>
          <Text style={styles.appInfoText}>
            Built with React Native & Convex
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.systemBackground,
  },
  scrollContainer: {
    paddingHorizontal: 24,
    paddingBottom: 24,
  },
  header: {
    marginTop: 16,
    marginBottom: 24,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: Colors.label,
  },
  userCard: {
    backgroundColor: Colors.secondarySystemBackground,
    borderRadius: 16,
    padding: 20,
    marginBottom: 24,
    flexDirection: 'row',
    alignItems: 'center',
  },
  avatarContainer: {
    marginRight: 16,
  },
  avatar: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: Colors.systemBackground,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: Colors.primary,
  },
  userInfo: {
    flex: 1,
  },
  userName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: Colors.label,
    marginBottom: 4,
  },
  userEmail: {
    fontSize: 16,
    color: Colors.secondaryLabel,
  },
  menuSection: {
    marginBottom: 32,
  },
  menuItem: {
    backgroundColor: Colors.secondarySystemBackground,
    borderRadius: 12,
    padding: 16,
    marginBottom: 8,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  menuItemContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  menuItemIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: Colors.systemBackground,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  menuItemText: {
    fontSize: 16,
    fontWeight: '500',
    color: Colors.label,
  },
  signOutSection: {
    marginBottom: 24,
  },
  signOutButton: {
    borderColor: Colors.error,
  },
  signOutButtonText: {
    color: Colors.error,
  },
  appInfo: {
    alignItems: 'center',
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: Colors.separator,
  },
  appInfoText: {
    fontSize: 12,
    color: Colors.tertiaryLabel,
    marginBottom: 4,
  },
});