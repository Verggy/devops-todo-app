import jenkins.model.*
import hudson.security.*

def instance = Jenkins.getInstance()

// Configure security realm
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
def adminPassword = new File('/run/secrets/jenkins-admin-password').text.trim()
hudsonRealm.createAccount('admin', adminPassword)
instance.setSecurityRealm(hudsonRealm)

// Configure authorization strategy
def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
instance.setAuthorizationStrategy(strategy)

// Save the state
instance.save()
