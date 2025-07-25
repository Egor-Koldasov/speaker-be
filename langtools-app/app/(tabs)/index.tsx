import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from 'convex/react';
import { api } from '../../convex/_generated/api.js';
import { Colors } from '@/constants/Colors';

export default function HomeScreen(): JSX.Element {
  
  // Get current user data
  const currentUser = useQuery(api.users.getCurrentUser);

  const getGreeting = (): string => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  };

  const userName = (currentUser && 'name' in currentUser) ? currentUser.name || 'there' : 'there';

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.greeting}>
            {getGreeting()}, {userName}! 👋
          </Text>
          <Text style={styles.subtitle}>
            Ready to continue your language learning journey?
          </Text>
        </View>

        {/* Welcome Card */}
        <View style={styles.welcomeCard}>
          <View style={styles.cardHeader}>
            <Ionicons name="sparkles" size={24} color={Colors.primary} />
            <Text style={styles.cardTitle}>Welcome to Langtools!</Text>
          </View>
          <Text style={styles.cardDescription}>
            You're successfully logged in to the Langtools mobile app. 
            This is your dashboard where you'll access all your language learning tools.
          </Text>
          <View style={styles.statusBadge}>
            <Ionicons name="checkmark-circle" size={16} color={Colors.success} />
            <Text style={styles.statusText}>Authentication Active</Text>
          </View>
        </View>

        {/* Feature Cards */}
        <View style={styles.featuresSection}>
          <Text style={styles.sectionTitle}>Coming Soon</Text>
          
          <TouchableOpacity style={styles.featureCard} disabled>
            <View style={styles.featureIcon}>
              <Ionicons name="book-outline" size={24} color={Colors.primary} />
            </View>
            <View style={styles.featureContent}>
              <Text style={styles.featureTitle}>Vocabulary Builder</Text>
              <Text style={styles.featureDescription}>
                Create and study custom vocabulary lists
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={Colors.tertiaryLabel} />
          </TouchableOpacity>

          <TouchableOpacity style={styles.featureCard} disabled>
            <View style={styles.featureIcon}>
              <Ionicons name="chatbubbles-outline" size={24} color={Colors.primary} />
            </View>
            <View style={styles.featureContent}>
              <Text style={styles.featureTitle}>AI Conversations</Text>
              <Text style={styles.featureDescription}>
                Practice speaking with AI language partners
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={Colors.tertiaryLabel} />
          </TouchableOpacity>

          <TouchableOpacity style={styles.featureCard} disabled>
            <View style={styles.featureIcon}>
              <Ionicons name="trophy-outline" size={24} color={Colors.primary} />
            </View>
            <View style={styles.featureContent}>
              <Text style={styles.featureTitle}>Progress Tracking</Text>
              <Text style={styles.featureDescription}>
                Monitor your learning progress and achievements
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={Colors.tertiaryLabel} />
          </TouchableOpacity>
        </View>

        {/* User Info */}
        {currentUser && 'email' in currentUser && (
          <View style={styles.userInfo}>
            <Text style={styles.userInfoTitle}>Account Information</Text>
            <View style={styles.userInfoRow}>
              <Text style={styles.userInfoLabel}>Email:</Text>
              <Text style={styles.userInfoValue}>{currentUser.email}</Text>
            </View>
            {'name' in currentUser && currentUser.name && (
              <View style={styles.userInfoRow}>
                <Text style={styles.userInfoLabel}>Name:</Text>
                <Text style={styles.userInfoValue}>{currentUser.name}</Text>
              </View>
            )}
          </View>
        )}
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
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: Colors.label,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: Colors.secondaryLabel,
    lineHeight: 22,
  },
  welcomeCard: {
    backgroundColor: Colors.secondarySystemBackground,
    borderRadius: 16,
    padding: 20,
    marginBottom: 24,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: Colors.label,
    marginLeft: 8,
  },
  cardDescription: {
    fontSize: 16,
    color: Colors.secondaryLabel,
    lineHeight: 22,
    marginBottom: 16,
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    backgroundColor: Colors.successBackground,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  statusText: {
    fontSize: 14,
    color: Colors.success,
    fontWeight: '500',
    marginLeft: 4,
  },
  featuresSection: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: Colors.label,
    marginBottom: 16,
  },
  featureCard: {
    backgroundColor: Colors.secondarySystemBackground,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    opacity: 0.6,
  },
  featureIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: Colors.systemBackground,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 16,
  },
  featureContent: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.label,
    marginBottom: 4,
  },
  featureDescription: {
    fontSize: 14,
    color: Colors.secondaryLabel,
  },
  userInfo: {
    backgroundColor: Colors.secondarySystemBackground,
    borderRadius: 12,
    padding: 16,
  },
  userInfoTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: Colors.label,
    marginBottom: 12,
  },
  userInfoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  userInfoLabel: {
    fontSize: 14,
    color: Colors.secondaryLabel,
    width: 60,
  },
  userInfoValue: {
    fontSize: 14,
    color: Colors.label,
    flex: 1,
    fontWeight: '500',
  },
});